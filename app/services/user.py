from fastapi import HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas.user import CreateUser
from app.tools.mongo import mongo_service


class UserService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def create_user(self, data: CreateUser):
        existing_user = await self.db["users"].find_one({"email": data.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists.")

        inserted_user = await self.db["users"].insert_one(data.model_dump())
        print(inserted_user.inserted_id)


# Dependency Injection Function
def get_user_service(db: AsyncIOMotorDatabase = Depends(lambda: mongo_service.db)):
    return UserService(db)
