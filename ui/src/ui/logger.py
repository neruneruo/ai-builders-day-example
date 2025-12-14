import logging
import os
import sys

import streamlit as st

from dotenv import load_dotenv

load_dotenv()


def _init_logger() -> logging.Logger:
    """
    Reset logger component
    """
    logger = logging.getLogger("StreamlitApp")

    # 既存ハンドラを外す（コピーしたリストを回す）
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()

    logger.setLevel(
        getattr(
            logging, os.getenv("APPLICATION_LOG_LEVEL", "INFO").upper(), logging.INFO
        )
    )
    logger.propagate = False
    logger.addHandler(handler := logging.StreamHandler(sys.stdout))
    handler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))

    return logger


def init() -> logging.Logger:
    logger = logging.getLogger("StreamlitApp")
    new_log_level = getattr(
        logging, os.getenv("APPLICATION_LOG_LEVEL", "INFO").upper(), logging.INFO
    )

    if not logger.handlers:
        logger = _init_logger()
    elif logger.getEffectiveLevel() != new_log_level:
        logger = _init_logger()
        st.info(f"Reset log level to {logging.getLevelName(new_log_level)}")

    return logger


def debug(msg, *args, **kwargs):
    logging.getLogger("StreamlitApp").debug(msg, *args, **kwargs)
    if logging.getLogger("StreamlitApp").isEnabledFor(logging.DEBUG):
        st.caption(msg)


def info(msg, *args, **kwargs):
    logging.getLogger("StreamlitApp").info(msg, *args, **kwargs)
    if logging.getLogger("StreamlitApp").isEnabledFor(logging.INFO):
        st.info(msg)


def jsoninfo(msg, *args, **kwargs):
    logging.getLogger("StreamlitApp").info(msg, *args, **kwargs)
    if logging.getLogger("StreamlitApp").isEnabledFor(logging.INFO):
        st.json(msg)


def warning(msg, *args, **kwargs):
    logging.getLogger("StreamlitApp").warning(msg, *args, **kwargs)
    if logging.getLogger("StreamlitApp").isEnabledFor(logging.WARNING):
        st.warning(msg)


def error(msg, *args, **kwargs):
    logging.getLogger("StreamlitApp").error(msg, *args, **kwargs)
    if logging.getLogger("StreamlitApp").isEnabledFor(logging.ERROR):
        st.error(msg)
