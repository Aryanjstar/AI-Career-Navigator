import logging
from functools import wraps
from typing import Any, Callable, TypeVar, cast

from quart import current_app, request

from error import error_response


def authenticated_path(route_fn: Callable[[str, dict[str, Any]], Any]):
    """
    Simplified decorator for routes that request a specific file (no authentication required)
    """

    @wraps(route_fn)
    async def auth_handler(path=""):
        # No authentication required - just pass empty auth claims
        auth_claims = {}
        return await route_fn(path, auth_claims)

    return auth_handler


_C = TypeVar("_C", bound=Callable[..., Any])


def authenticated(route_fn: _C) -> _C:
    """
    Simplified decorator for routes (no authentication required)
    """

    @wraps(route_fn)
    async def auth_handler(*args, **kwargs):
        # No authentication required - just pass empty auth claims
        auth_claims = {}
        return await route_fn(auth_claims, *args, **kwargs)

    return cast(_C, auth_handler)
