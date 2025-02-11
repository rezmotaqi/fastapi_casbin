# Entry point for FastAPI app
from fastapi import FastAPI

from app.routes import auth, user, general

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(general.router, prefix="/general", tags=["General"])
