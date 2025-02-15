import tempfile

import casbin
from fastapi import Request, Depends, HTTPException

from app.services.auth import get_auth_service
from app.tools.mongo import mongo_service


class CasbinService:
	"""Handles role-based access control using Casbin with MongoDB"""

	def __init__(self):
		self.enforcer = None
		self.db = mongo_service.db

	def get_default_model(self):
		"""Returns a basic Casbin model as a string"""
		return """
        [request_definition]
        r = sub, obj, act

        [policy_definition]
        p = sub, obj, act

        [role_definition]
        g = _, _

        [policy_effect]
        e = some(where (p.eft == allow))

        [matchers]
        m = r.sub == p.sub && r.obj == p.obj && r.act == p.act
        """

	async def init_casbin(self):
		"""Initialize Casbin with a model and policy data from MongoDB"""
		model_text = self.get_default_model()

		# Create a temporary file to store the model
		with tempfile.NamedTemporaryFile(delete=False, mode='w',
										 encoding='utf-8') as model_file:
			model_file.write(model_text)
			model_path = model_file.name  # Get the path of the temporary file

		self.enforcer = casbin.Enforcer(model_path, None)

	async def load_policy(self):
		"""Load Casbin policies from MongoDB"""
		policies = await self.db.casbin_policies.find().to_list(length=1000)
		await self.init_casbin()
		for policy in policies:
			self.enforcer.add_policy(policy["role"], policy["resource"],
									 policy["action"])

	async def authorize(self, request: Request,
						token_data: dict = Depends(
							get_auth_service().verify_token)):
		"""Check if user is authorized based on Casbin policies."""

		await self.load_policy()
		email = token_data.get("sub")
		roles = await self.get_user_roles(email)

		resource = request.url.path.rstrip('/')
		action = request.method
		print(
			f"Checking authorization for roles: {roles} on resource: "
			f"{resource} with action: {action}")

		for role in roles:
			if self.enforcer.enforce(role, resource, action):
				return token_data  # User is authorized to access this
		# resource

		raise HTTPException(status_code=403, detail="Access denied")

	async def get_user_roles(self, email: str):
		"""Fetch user roles from MongoDB"""
		user = await self.db.users.find_one({"email": email})
		return user["roles"] if user else []


def get_casbin_service():
	return CasbinService()
