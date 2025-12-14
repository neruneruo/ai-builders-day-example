import time
import uuid

import streamlit as st

import ui.logger as logger

from ui.authentication import login_link, handle_callback, logout_link
from ui.agentcore_wrapper import agentcore_client, invoke_agentcore
from ui.init import init

from dotenv import load_dotenv

load_dotenv()

logger.init()

session_id = str(uuid.uuid4())
logger.info(f"session_id: {session_id}")

agent_core_client = agentcore_client()

handle_callback()


def main():
    init(agent_core_client, session_id)

    if not st.session_state.get("oauth_token"):
        st.info("ログイン中……")
        login_link()
        st.stop()

    header_container = st.container()
    history_container = st.container()
    current_container = st.container()
    footer_container = st.container()

    with header_container:
        title = "Amazon Bedrock AgentCoreサンプル"
        st.set_page_config(page_title="Amazon Bedrock AgentCoreサンプル", layout="wide")
        st.title(title)
        st.info("入力内容を要約するエージェントです")

    with history_container:
        for messages in st.session_state.get("messages", []):
            with st.chat_message(messages["role"]):
                if messages["role"] == "user":
                    st.markdown(messages["content"][0]["text"])
                else:
                    st.markdown(messages["content"])

    with current_container:
        messages = st.session_state.messages
        if messages and messages[-1].get("role") == "user":
            with st.chat_message("assistant"):
                placeholder = st.empty()
                answer = ""
                message_stop = False
                for chunk in invoke_agentcore(st.session_state.session_id):
                    event = chunk.get("event", None)
                    if event == "contentBlockDelta":
                        if message_stop:
                            placeholder.empty()
                            answer = ""
                            message_stop = False
                        answer += chunk.get("text", "")
                        placeholder.markdown(answer)
                        time.sleep(0.02)
                    elif event == "messageStop":
                        message_stop = True

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

    with footer_container:
        if prompt := st.chat_input("要約したい文章を入力"):
            st.session_state.user_input = [{"text": prompt}]
            st.session_state.messages.append(
                {"role": "user", "content": st.session_state.user_input}
            )
            st.rerun()

        logout_link()


if __name__ == "__main__":
    main()
