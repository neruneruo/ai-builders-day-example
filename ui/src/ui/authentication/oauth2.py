import hashlib
import os
import secrets

import streamlit as st

from urllib.parse import urlencode

from authlib.integrations.requests_client import OAuth2Session

from ui.authentication.util import _b64url_encode, _make_state, _verify_state
import ui.logger as logger


def _get_oauth_session():
    return OAuth2Session(
        client_id=st.secrets["auth0"]["client_id"],
        client_secret=st.secrets["auth0"]["client_secret"],
        token_endpoint_auth_method="client_secret_post",
    )


def _ensure_pkce() -> tuple[str, str]:
    verifier = _b64url_encode(os.urandom(40))
    challenge = _b64url_encode(hashlib.sha256(verifier.encode("ascii")).digest())
    return verifier, challenge


def login_link():
    nonce = secrets.token_urlsafe(16)
    pkce_verifier, pkce_challenge = _ensure_pkce()

    auth_provider = os.environ.get("AUTH_PROVIDER", "auth0")

    state = _make_state(
        {
            "nonce": nonce,
            "pkce_verifier": pkce_verifier,
        }
    )

    params = {
        "response_type": "code",
        "response_mode": "query",
        "client_id": st.secrets[auth_provider]["client_id"],
        "redirect_uri": st.secrets[auth_provider]["oauth2"]["redirect_uri"],
        "scope": st.secrets[auth_provider]["oauth2"].get("scope", ""),
        "state": state,
        "code_challenge": pkce_challenge,
        "code_challenge_method": "S256",
        # "prompt": "consent",
        **({"audience": st.secrets[auth_provider]["audience"]} if st.secrets[auth_provider]["audience"] else {}),  # fmt: skip
    }
    url = f"https://{st.secrets[auth_provider]["auth_domain"]}/{st.secrets[auth_provider]["oauth2"]["auth_endpoint"]}?{urlencode(params)}"

    st.markdown(
        f'<meta http-equiv="refresh" content="0; url={url}">',
        unsafe_allow_html=True,
    )


def handle_callback():
    logger.debug("oauth2_callback() called")
    logger.info(st.query_params)

    qp = st.query_params
    code = qp.get("code")
    state = qp.get("state")
    if not code:
        logger.info("no code.")
        return False
    logger.info(f"state: {state}")
    logger.info(f"session_state: {st.session_state.get("oauth_state")}")

    body = _verify_state(state) if state else None
    if not body:
        st.error("Invalid or expired state")
        return True

    pkce_verifier = body.get("pkce_verifier")
    if not pkce_verifier:
        st.error("Missing PKCE verifier in state")
        return True

    client = _get_oauth_session()
    token = client.fetch_token(
        url=f"https://{st.secrets["auth0"]["auth_domain"]}/{st.secrets["auth0"]["oauth2"]["token_endpoint"]}",
        grant_type="authorization_code",
        code=code,
        redirect_uri=st.secrets["auth0"]["oauth2"]["redirect_uri"],
        code_verifier=pkce_verifier,
    )

    st.session_state.oauth_token = token
    st.query_params.clear()
    st.rerun()
    return True


def logout_link() -> None:
    logout_url = f"https://{st.secrets["auth0"]["auth_domain"]}/v2/logout?" + urlencode(
        {
            "client_id": st.secrets["auth0"]["client_id"],
            "returnTo": st.secrets["auth0"]["oauth2"]["redirect_uri"],
        }
    )

    st.markdown(
        f'<a href="{logout_url}">ログアウト</a>',
        unsafe_allow_html=True,
    )
