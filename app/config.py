# Configuration settings
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
	CLIENT_ID = os.getenv("CLIENT_ID")
	CLIENT_SECRET = os.getenv("CLIENT_SECRET")
	TOKEN_ENDPOINT = os.getenv("TOKEN_ENDPOINT")
	REDIRECT_URI = os.getenv("REDIRECT_URI")
	SECRET_KEY = os.getenv("SECRET_KEY")
	MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
	REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
	MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")



config = Config()
