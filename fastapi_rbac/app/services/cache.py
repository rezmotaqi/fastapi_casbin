# Redis Caching Service
from fastapi import HTTPException

from fastapi_rbac.app.interfaces.cache import CacheInterface
from fastapi_rbac.app.tools.redis import redis_service


class RedisCache(CacheInterface):
	"""Handles caching using Redis"""

	async def get(self, key: str):
		return await redis_service.db.get(key)

	async def set(self, key: str, value: str, expiration: int = 300):
		await redis_service.db.setex(key, expiration, value)

	async def invalidate(self, key: str):
		await redis_service.db.delete(key)

	@staticmethod
	async def clear_cache():
		try:
			# Clear the entire Redis database
			await redis_service.db.flushall()
		except Exception as e:
			raise HTTPException(status_code=500,
								detail=f"Error clearing cache: {e}")


redis_cache = RedisCache()
