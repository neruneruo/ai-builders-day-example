from . import app
from . import logger

import boto3
import json
import logging
import os

from bedrock_agentcore import RequestContext
from bedrock_agentcore.memory.integrations.strands.config import AgentCoreMemoryConfig  # fmt: skip  # noqa: E501
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager  # fmt: skip  # noqa: E501
from strands import Agent
from strands.models import BedrockModel

from .context import get_jwt_claims_from_context
from .init import dump_environment_variables


# Initialize General
logger = logging.getLogger("AgentApp")

# Initialize Amazon Bedrock
session = boto3.Session(
    region_name=os.environ.get("AWS_BEDROCK_REGION", "ap-northeast-1"),
)

bedrock_model = BedrockModel(
    boto_session=session,
    model_id=os.environ.get(
        "AWS_BEDROCK_MODEL", "jp.anthropic.claude-sonnet-4-5-20250929-v1:0"
    ),
    cache_prompt="default",
)


def _init_agentcore_memory(
    session_id: str, context: RequestContext
) -> AgentCoreMemorySessionManager | None:
    jwt_claims = get_jwt_claims_from_context(context)
    actor_id = jwt_claims["sub"].replace("|", "_")

    agentcore_memory_config = AgentCoreMemoryConfig(
        memory_id=os.environ["AWS_BEDROCK_AGENTCORE_MEMORY_ID"],
        session_id=session_id,
        actor_id=actor_id,
    )

    return AgentCoreMemorySessionManager(
        region_name=os.environ["AWS_REGION"],
        agentcore_memory_config=agentcore_memory_config,
    )


# Main
async def main(payload, context: RequestContext):
    dump_environment_variables()

    logger.debug(f"payload: {payload}")
    logger.debug(f"context: {context}")

    session_id = getattr(context, "session_id", None)
    logger.info(f"session_id: {session_id}")

    session_manager = None
    if os.environ.get("AWS_BEDROCK_AGENTCORE_MEMORY_ID", None):
        session_manager = _init_agentcore_memory(session_id, context)

    system_prompt = """
You are AI assistant. You are a document summarize specialist.

Summarize what was presented in the prompt.
Output should be in the same language as entered at the prompt.
"""

    messages = []

    async def stream():
        agent = Agent(
            model=bedrock_model,
            system_prompt=system_prompt,
            messages=messages,
            **({"session_manager": session_manager} if session_manager else {}),
        )

        try:
            parts = payload.get("prompt", [])
            logger.info(f"payload: {parts}")

            user_message = []
            for block in json.loads(parts):
                logger.info(f"block: {block}")

                if "text" in block:
                    user_message.append({"text": block["text"]})
            logger.info(f"user_message: {user_message}")

            async for chunk in agent.stream_async(user_message):
                yield chunk

        except Exception as e:
            logger.error(f"agent() error: {e}", exc_info=True)
            yield {"result": f"agent() error: {e}"}

    return stream()


@app.entrypoint
async def entrypoint(payload, context: RequestContext):
    async for event in await main(payload, context):
        yield event
