from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import config
from app.interfaces.singleton import BaseSingleton


class MongoDBConnection(BaseSingleton):
	def __init__(self):
		self._client = None

	@property
	def client(self) -> AsyncIOMotorClient:
		""" Lazily initialize the MongoDB client when it's first accessed """
		if not self._client:
			try:
				# Initialize MongoDB client with connection URI from config
				self._client = AsyncIOMotorClient(config.MONGO_URI)
				print("MongoDB connection established.")
			except Exception as e:
				print(f"Error connecting to MongoDB: {e}")
				raise
		return self._client

	@property
	def db(self) -> AsyncIOMotorDatabase:
		""" Property to access the MongoDB database instance """
		return self.client[config.MONGO_DB_NAME]


# Singleton instance for MongoDB
mongo_service = MongoDBConnection()
