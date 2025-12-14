import base64
import hashlib
import hmac
import json
import os
import time

import streamlit as st

APP_SECRET = (
    os.getenv("APP_SECRET")
    or st.secrets.get("app_secret")
    or (st.get_option("server.cookieSecret") or "dev-only-fallback")
).encode("utf-8")


def _b64url_encode(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode("ascii")


def _b64url_decode(s: str) -> bytes:
    pad = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + pad)


def _make_state(payload: dict, ttl_sec: int = 600) -> str:
    body = payload.copy()
    now = int(time.time())
    body.setdefault("iat", now)
    body.setdefault("exp", now + ttl_sec)
    body_bytes = json.dumps(body, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )
    body_b64 = _b64url_encode(body_bytes)
    sig = hmac.new(APP_SECRET, body_b64.encode("ascii"), hashlib.sha256).digest()
    sig_b64 = _b64url_encode(sig)
    return f"{body_b64}.{sig_b64}"


def _verify_state(state: str) -> dict | None:
    try:
        body_b64, sig_b64 = state.split(".", 1)
        expected = hmac.new(
            APP_SECRET, body_b64.encode("ascii"), hashlib.sha256
        ).digest()
        if not hmac.compare_digest(expected, _b64url_decode(sig_b64)):
            return None
        body = json.loads(_b64url_decode(body_b64))
        now = int(time.time())
        if body.get("exp") is None or now > int(body["exp"]):
            return None
        return body
    except Exception:
        return None
