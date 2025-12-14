import os
import logging

logger = logging.getLogger("AgentApp")

environment_variable_keys = [
    "AWS_REGION",
    "AWS_BEDROCK_MODEL",
    "AWS_BEDROCK_AGENTCORE_MEMORY_ID",
    "STRANDS_LOG_LEVEL",
    "AGENT_LOG_LEVEL",
]


def dump_environment_variables() -> None:
    logger.info("Environment variables:")
    for environment_variable_key in environment_variable_keys:
        logger.info(
            f"  {environment_variable_key}: {os.environ.get(environment_variable_key)}"
        )
