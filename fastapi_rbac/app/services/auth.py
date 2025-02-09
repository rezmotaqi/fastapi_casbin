# Authentication Service
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException

from fastapi_rbac.app.config import config
from fastapi_rbac.app.interfaces.auth import AuthInterface
from fastapi_rbac.app.tools.mongo import mongo_service


class AuthService(AuthInterface):
	"""Handles authentication logic"""

	async def get_user_roles(self, email: str):
		"""Fetch user roles from MongoDB"""
		user = await mongo_service.get_db().users.find_one({"email": email})
		return user["roles"] if user else []

	async def create_access_token(self, data: dict):
		"""Generate JWT token"""
		expire = datetime.now(timezone.utc) + timedelta(minutes=30)
		data.update({"exp": expire})
		return jwt.encode(data, config.SECRET_KEY, algorithm="HS256")

	async def verify_token(self, token: str):
		"""Decode and validate JWT token"""
		try:
			return jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
		except jwt.ExpiredSignatureError:
			raise HTTPException(status_code=401, detail="Token expired")
		except jwt.InvalidTokenError:
			raise HTTPException(status_code=401, detail="Invalid token")


auth_service = AuthService()
