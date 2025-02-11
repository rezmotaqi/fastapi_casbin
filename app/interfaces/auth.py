# Interface for authentication
from abc import ABC, abstractmethod

from fastapi import Header


class AuthInterface(ABC):
	"""Abstract class for authentication services"""

	@abstractmethod
	async def get_user_roles(self, email: str):
		pass

	@abstractmethod
	async def create_access_token(self, data: dict):
		pass

	@abstractmethod
	async def verify_token(self, authorization: Header(...)):
		pass

