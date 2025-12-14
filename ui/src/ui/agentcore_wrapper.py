import boto3
import json
import os
import requests
import streamlit as st

from urllib.parse import urlsplit, urlunsplit, quote
from sseclient import SSEClient
from typing import Iterator, Any


def _mock_endpoint(request, **kwargs):
    parts = urlsplit(request.url)
    new_parts = (parts.scheme, parts.netloc, "/invocations", "", parts.fragment)
    request.url = urlunsplit(new_parts)


def agentcore_client():
    local_endpoint = os.environ.get("LOCAL_ENDPOINT", None)

    agent_core_client = boto3.client(
        "bedrock-agentcore",
        region_name=os.environ["AWS_REGION"],
        **({"endpoint_url": "http://localhost:8080/"} if local_endpoint else {}),
    )

    if local_endpoint:
        agent_core_client.meta.events.register("before-sign.*.*", _mock_endpoint)

    return agent_core_client


def _get_agentcore_endpoint() -> str:
    if os.environ.get("LOCAL_ENDPOINT"):
        return "http://localhost:8080/invocations"

    return f"https://bedrock-agentcore.{os.environ.get("AWS_REGION")}.amazonaws.com/runtimes/{quote(os.environ.get("AGENT_RUNTIME_ARN"), safe="")}/invocations?qualifier=DEFAULT"


def _get_headers(session_id: str) -> dict:
    token = st.session_state.oauth_token["access_token"]

    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Amzn-Bedrock-AgentCore-Runtime-Session-Id": session_id,
    }


def _get_data() -> str:
    data = {"prompt": json.dumps(st.session_state.user_input)}
    return json.dumps(data)


def _dump_response_error(response) -> None:
    st.error("サーバからJSON以外の応答が返りました。")
    st.write("status:", response.status_code)
    st.write("headers:", dict(response.headers))
    st.write("body:", response.text[:1000])


def invoke_agentcore(session_id: str) -> Iterator[dict[str, Any]]:
    st_ph = st.empty()
    state = "running"

    with st_ph.status("分析中…", state=state) as status:
        response = requests.post(
            _get_agentcore_endpoint(),
            headers=_get_headers(session_id),
            data=_get_data(),
            stream=True,
        )
        response.raise_for_status()

        try:
            if "text/event-stream" not in (response.headers.get("Content-Type") or ""):
                yield {"event": "message", "data": response.text}
                return

            client = SSEClient(response)

            for event in client.events():
                if not event.data:
                    continue
                try:
                    data = json.loads(event.data)
                    if isinstance(data, dict):
                        data_event = data.get("event", {})

                        if data_event.get("contentBlockDelta", {}):
                            text = (
                                data_event.get("contentBlockDelta", {})
                                .get("delta", {})
                                .get("text")
                            )
                            if text:
                                if state == "running":
                                    state = "complete"
                                    status.update(label=None, state=state)
                                    st_ph.empty()

                                yield {"event": "contentBlockDelta", "text": text}
                        if data_event.get("messageStop", {}):
                            yield {"event": "messageStop"}
                except json.JSONDecodeError:
                    continue
        except ValueError:
            _dump_response_error()
            raise
