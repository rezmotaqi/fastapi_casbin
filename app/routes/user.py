# User Routes

from fastapi import APIRouter, Depends

from app.schemas.user import CreateUser
from app.services.user import UserService, get_user_service
from app.services.casbin import get_casbin_service
router = APIRouter()


@router.post("/", dependencies=[Depends(get_casbin_service().authorize)])
async def create_user(
		data: CreateUser,
		user_service: UserService = Depends(get_user_service)
):
	await user_service.create_user(data=data)
	return {"message": "User created successfully"}
