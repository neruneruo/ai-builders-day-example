import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()

"""
Strands Agents logger settings
"""
logging.getLogger("strands").setLevel(
    getattr(logging, os.getenv("STRANDS_LOG_LEVEL", "INFO").upper(), logging.INFO)
)
logging.getLogger("strands").addHandler(handler := logging.StreamHandler(sys.stdout))
handler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))

"""
Agent Application logger settings
"""
logging.getLogger("AgentApp").setLevel(
    getattr(logging, os.getenv("AGENT_LOG_LEVEL", "INFO").upper(), logging.INFO)
)
logging.getLogger("AgentApp").propagate = False
logging.getLogger("AgentApp").addHandler(handler := logging.StreamHandler(sys.stdout))
handler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))
