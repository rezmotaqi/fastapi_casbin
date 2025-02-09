from fastapi import HTTPException
from typing import List

from fastapi_rbac.app.tools.mongo import mongo_service


class UserService:
	def __init__(self, db=mongo_service.get_db()):
		self.db = db

	async def create_user(self, username: str, email: str, roles: List[str]):
		# Check if the user already exists
		existing_user = await self.db["users"].find_one({"email": email})
		if existing_user:
			raise HTTPException(status_code=400,
								detail="User with this email already exists.")

		# Create the new user document
		user = {
			"username": username,
			"email": email,
			"roles": roles
		}

		# Insert the user into the database
		await self.db["users"].insert_one(user)
		return user
