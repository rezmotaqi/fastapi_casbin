# Authentication Service
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, Header

from app.config import config
from app.interfaces.auth import AuthInterface
from app.tools.mongo import mongo_service


class AuthService(AuthInterface):
    """Handles authentication logic"""

    async def get_user_roles(self, email: str):
        """Fetch user roles from MongoDB"""
        user = await mongo_service.db.users.find_one({"email": email})
        return user["roles"] if user else []

    async def create_access_token(self, data: dict):
        """Generate JWT token"""
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
        data.update({"exp": expire})
        return jwt.encode(data, config.SECRET_KEY, algorithm="HS256")

    async def verify_token(self, authorization: str = Header(...)):
        """Dependency to verify JWT token and return token data."""
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        token = authorization.split(" ")[1]

        try:
            return jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")


def get_auth_service():
    return AuthService()