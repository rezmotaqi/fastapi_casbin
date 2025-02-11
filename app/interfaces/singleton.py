from abc import ABC, abstractmethod


class SingletonInterface(ABC):
	"""This is the Singleton Interface that guarantees that a class
	implementing it will follow the Singleton pattern."""

	@abstractmethod
	def get_instance(cls):
		"""Abstract method to get the instance of the singleton class"""
		pass


class BaseSingleton(SingletonInterface):
	"""Base class for Singleton pattern. All classes inheriting from this
	will be Singletons."""

	_instance = None

	def __new__(cls, *args, **kwargs):
		"""Override __new__ to control the instantiation process"""
		if cls._instance is None:
			cls._instance = super().__new__(cls)
			print(f"Creating instance of {cls.__name__}")
		return cls._instance

	@classmethod
	def get_instance(cls):
		"""This method returns the singleton instance"""
		if cls._instance is None:
			cls._instance = cls()
			print(f"Creating instance of {cls.__name__}")
		return cls._instance
