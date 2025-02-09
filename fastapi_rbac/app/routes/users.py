# User Routes
from typing import List

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from fastapi_rbac.app.config import config
from fastapi_rbac.app.services.casbin import casbin_service
from fastapi_rbac.app.services.user import UserService

router = APIRouter()


# @router.post("/", dependencies=[Depends(casbin_service.authorize)])
# async def create_user(email: str):
# 	return {"message": f"User {email} created"}


@router.post("")
async def create_user(
		username: str,
		email: str,
		roles: List[str],
		user_service: UserService = Depends()
):
	# c = AsyncIOMotorClient(config.MONGO_URI, maxPoolSize=100,
	# 				   minPoolSize=10)
	# d = c['rbac_db']
	# user = await d.users.insert_one(username, email, roles)

	user = await user_service.create_user(username, email, roles)
	return {"message": "User created successfully", "user": user}
