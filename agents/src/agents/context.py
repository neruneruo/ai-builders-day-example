import jwt
import json
import logging

from bedrock_agentcore import RequestContext


logger = logging.getLogger("AgentApp")


def get_jwt_claims_from_context(context: RequestContext):
    """
    Extract JWT claims from the given context variable.

    Assumes that the Authorization header is always present,
    since authentication has already been performed.
    """
    try:
        claims = jwt.decode(
            context.request_headers.get("Authorization").replace("Bearer ", ""),
            options={"verify_signature": False},
        )
        logger.debug(f"Claims: {json.dumps(claims)}")

        return claims
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid JWT token: {e}")
        return None
