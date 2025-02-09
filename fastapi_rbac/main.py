# Entry point for FastAPI app
from fastapi import FastAPI

from fastapi_rbac.app.routes import auth, users, general

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(general.router, prefix="/general", tags=["General"])

if __name__ == "__main__":
	import uvicorn

	uvicorn.run(
		app, host="127.0.0.1", port=8000,
		env_file="/Users/rez/PycharmProjects/fastapi_rbac/.env")
