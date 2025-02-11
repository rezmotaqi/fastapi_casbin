# User Routes

from fastapi import APIRouter, Depends

from app.schemas.user import CreateUser
from app.services.user import UserService

router = APIRouter()

# user_service = UserService()


# @router.post("/", dependencies=[Depends(casbin_service.authorize)])
@router.post("/")
async def create_user(
		data: CreateUser,
		user_service: UserService = Depends(UserService)
):
	user = await user_service.create_user(data=data)
	return {"message": "User created successfully"}
