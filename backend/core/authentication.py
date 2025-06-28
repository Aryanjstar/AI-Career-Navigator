"""
Simplified authentication helper for AI Career Navigator
"""
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class AuthError(Exception):
    """Exception for authentication errors"""
    pass


class AuthenticationHelper:
    """
    Simplified authentication helper that doesn't require actual authentication.
    """
    
    def __init__(self):
        self.enabled = False
    
    async def get_auth_claims_if_enabled(self, headers: Dict[str, str]) -> Dict[str, Any]:
        """Return empty auth claims since authentication is disabled"""
            return {}

    async def check_path_auth(self, path: str, auth_claims: Dict[str, Any], search_client: Any) -> bool:
        """Always allow access since authentication is disabled"""
            return True
