# Interface for caching
from abc import ABC, abstractmethod


class CacheInterface(ABC):
	"""Abstract class for caching services"""

	@abstractmethod
	async def get(self, key: str):
		pass

	@abstractmethod
	async def set(self, key: str, value: str, expiration: int = 300):
		pass

	@abstractmethod
	async def invalidate(self, key: str):
		pass


