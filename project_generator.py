import os

PROJECT_NAME = "fastapi_rbac"
SERVICES_FOLDER = f"{PROJECT_NAME}/app/services"
INTERFACES_FOLDER = f"{PROJECT_NAME}/app/interfaces"

# Ensure required folders exist
os.makedirs(SERVICES_FOLDER, exist_ok=True)
os.makedirs(INTERFACES_FOLDER, exist_ok=True)

# Required interface files
INTERFACE_FILES = {
	f"{INTERFACES_FOLDER}/auth_interface.py": """# Interface for authentication
from abc import ABC, abstractmethod

class AuthInterface(ABC):
    \"\"\"Abstract class for authentication services\"\"\"

    @abstractmethod
    async def get_user_roles(self, email: str):
        pass

    @abstractmethod
    async def create_access_token(self, data: dict):
        pass

    @abstractmethod
    async def verify_token(self, token: str):
        pass
""",

	f"{INTERFACES_FOLDER}/cache_interface.py": """# Interface for caching
from abc import ABC, abstractmethod

class CacheInterface(ABC):
    \"\"\"Abstract class for caching services\"\"\"

    @abstractmethod
    async def get(self, key: str):
        pass

    @abstractmethod
    async def set(self, key: str, value: str, expiration: int = 300):
        pass

    @abstractmethod
    async def invalidate(self, key: str):
        pass
"""
}

# Required service files
SERVICE_FILES = {
	f"{SERVICES_FOLDER}/auth_service.py": """# Authentication Service
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from app.database import db_instance
from app.config import config
from app.interfaces.auth_interface import AuthInterface

class AuthService(AuthInterface):
    \"\"\"Handles authentication logic\"\"\"

    async def get_user_roles(self, email: str):
        \"\"\"Fetch user roles from MongoDB\"\"\"
        user = await db_instance.db.users.find_one({"email": email})
        return user["roles"] if user else []

    async def create_access_token(self, data: dict):
        \"\"\"Generate JWT token\"\"\"
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
        data.update({"exp": expire})
        return jwt.encode(data, config.SECRET_KEY, algorithm="HS256")

    async def verify_token(self, token: str):
        \"\"\"Decode and validate JWT token\"\"\"
        try:
            return jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

auth_service = AuthService()
""",

	f"{SERVICES_FOLDER}/cache_service.py": """# Redis Caching Service
import redis.asyncio as redis
from app.config import config
from app.interfaces.cache_interface import CacheInterface

class RedisCache(CacheInterface):
    \"\"\"Handles caching using Redis\"\"\"

    def __init__(self):
        self.redis = redis.Redis.from_url(config.REDIS_URL, decode_responses=True)

    async def get(self, key: str):
        return await self.redis.get(key)

    async def set(self, key: str, value: str, expiration: int = 300):
        await self.redis.setex(key, expiration, value)

    async def invalidate(self, key: str):
        await self.redis.delete(key)

redis_cache = RedisCache()
""",

	f"{SERVICES_FOLDER}/casbin_service.py": """# Casbin Authorization Service
import casbin
from fastapi import Depends, Request, HTTPException
from app.database import db_instance, redis_cache

class CasbinService:
    \"\"\"Handles role-based access control using Casbin with MongoDB\"\"\"

    def __init__(self):
        self.enforcer = None  # Casbin enforcer will be initialized later

    async def load_policy(self):
        \"\"\"Load Casbin policies from MongoDB dynamically\"\"\"
        policies = db_instance.db.casbin_policies.find({})
        for policy in await policies.to_list(length=1000):
            self.enforcer.add_policy(policy["sub"], policy["obj"], policy["act"])

    async def init_casbin(self):
        \"\"\"Dynamically fetch Casbin model from MongoDB instead of a static file\"\"\"
        model_data = await db_instance.db.casbin_models.find_one({})
        if not model_data:
            raise Exception("Casbin model not found in MongoDB")

        with open("casbin_model.conf", "w") as f:
            f.write(model_data["model_text"])

        self.enforcer = casbin.Enforcer("casbin_model.conf")
        await self.load_policy()

    async def authorize(self, request: Request, token_data: dict):
        \"\"\"Check if user is authorized based on Casbin policies.\"\"\"
        email = token_data.get("sub")

        # Check cached roles first
        cached_roles = await redis_cache.redis.get(f"user_roles:{email}")
        if cached_roles:
            roles = cached_roles.split(",")
        else:
            # Fetch roles from MongoDB
            user = await db_instance.db.users.find_one({"email": email})
            roles = user["roles"] if user else []
            await redis_cache.redis.set(f"user_roles:{email}", ",".join(roles), ex=300)

        # Check permissions for each role
        for role in roles:
            if self.enforcer.enforce(role, request.url.path, request.method):
                return token_data

        raise HTTPException(status_code=403, detail="Access denied")

casbin_service = CasbinService()
"""
}


# Function to create missing interface and service files
def fix_project():
	# Create missing interface files
	for file, content in INTERFACE_FILES.items():
		with open(file, "w", encoding="utf-8") as f:
			f.write(content)

	# Create missing service files
	for file, content in SERVICE_FILES.items():
		with open(file, "w", encoding="utf-8") as f:
			f.write(content)

	print(
		"✅ Project fixed: Now using MongoDB for Casbin configuration and fully follows SOLID principles!")


if __name__ == "__main__":
	fix_project()
