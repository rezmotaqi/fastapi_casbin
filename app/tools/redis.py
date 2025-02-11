import redis.asyncio as redis

from app.config import config
from app.interfaces.singleton import BaseSingleton


# file


class RedisConnection(BaseSingleton):

	def __init__(self):
		try:
			# Initialize Redis client with connection URL from config
			self._redis = redis.Redis.from_url(config.REDIS_URL,
											   decode_responses=True)
			print("Redis connection established.")
		except Exception as e:
			print(f"Error connecting to Redis: {e}")
			raise

	@property
	def db(self):
		""" Property to access the Redis client instance """
		return self._redis


redis_service = RedisConnection()
