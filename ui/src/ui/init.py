import streamlit as st


def init(agent_core_client, session_id: str) -> None:
    """
    Initialize Streamlit session state variables.
    """

    if "client" not in st.session_state:
        st.session_state.client = agent_core_client

    if "session_id" not in st.session_state:
        st.session_state.session_id = session_id

    if "user_input" not in st.session_state:
        st.session_state.user_input = None

    if "messages" not in st.session_state:
        st.session_state.messages = []
