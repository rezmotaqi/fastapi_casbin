from motor.motor_asyncio import AsyncIOMotorClient

from fastapi_rbac.app.config import config
from fastapi_rbac.app.interfaces.singleton import BaseSingleton


class MongoDBConnection(BaseSingleton):
	def __init__(self):
		try:
			# Initialize MongoDB client with connection URI from config
			self._client = AsyncIOMotorClient(config.MONGO_URI, maxPoolSize=100,
										  minPoolSize=10)
			print("MongoDB connection established.")
		except Exception as e:
			print(f"Error connecting to MongoDB: {e}")
			raise

	@property
	def client(self):
		""" Property to access the MongoDB database instance """
		return self._client

	def get_db(self, db_name=config.MONGO_DB_NAME):
		return self._client[db_name]


# Singleton instance for MongoDB
mongo_service = MongoDBConnection()


print(mongo_service)
