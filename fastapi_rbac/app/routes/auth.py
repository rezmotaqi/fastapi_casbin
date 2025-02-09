# Authentication Routes
from fastapi import APIRouter

from fastapi_rbac.app.services.auth import AuthService

router = APIRouter()
auth_service = AuthService()


@router.post("/token")
async def generate_token(email: str):
	roles = await auth_service.get_user_roles(email)
	return {"access_token": await auth_service.create_access_token(
		{"sub": email, "roles": roles})}


