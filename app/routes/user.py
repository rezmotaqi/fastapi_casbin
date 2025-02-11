# User Routes

from fastapi import APIRouter, Depends

from app.schemas.user import CreateUser
from app.services.auth import auth_service
from app.services.casbin import casbin_service
from app.services.user import UserService

router = APIRouter()

user_service = UserService()


@router.post("/", dependencies=[Depends(casbin_service.authorize)])
async def create_user(data: CreateUser, token_data: dict = Depends(auth_service.verify_token)):
	user = await user_service.create_user(data=data)
	return {"message": "User created successfully"}
