# Casbin Authorization Service
import casbin
from fastapi import Request, HTTPException

from app.services.cache import redis_cache
from app.tools.mongo import mongo_service


class CasbinService:
	"""Handles role-based access control using Casbin with MongoDB"""

	def __init__(self):
		self.enforcer = None  # Casbin enforcer will be initialized later

	async def load_policy(self):
		"""Load Casbin policies from MongoDB dynamically"""
		policies = mongo_service.db.casbin_policies.find({})
		for policy in await policies.to_list(length=1000):
			self.enforcer.add_policy(policy["sub"], policy["obj"],
									 policy["act"])

	async def init_casbin(self):
		"""Dynamically fetch Casbin model from MongoDB instead of a static
		file"""
		model_data = await mongo_service.db.casbin_models.find_one({})
		if not model_data:
			raise Exception("Casbin model not found in MongoDB")

		with open("casbin_model.conf", "w") as f:
			f.write(model_data["model_text"])

		self.enforcer = casbin.Enforcer("casbin_model.conf")
		await self.load_policy()

	async def authorize(self, request: Request, token_data: dict):
		"""Check if user is authorized based on Casbin policies."""
		email = token_data.get("sub")

		# Check cached roles first
		cached_roles = await redis_cache.get(f"user_roles:{email}")
		if cached_roles:
			roles = cached_roles.split(",")
		else:
			# Fetch roles from MongoDB
			user = await mongo_service.db.users.find_one({"email": email})
			roles = user["roles"] if user else []
			await redis_cache.set(f"user_roles:{email}", ",".join(
				roles),
										expiration=300)

		# Check permissions for each role
		for role in roles:
			if self.enforcer.enforce(role, request.url.path, request.method):
				return token_data

		raise HTTPException(status_code=403, detail="Access denied")


casbin_service = CasbinService()
