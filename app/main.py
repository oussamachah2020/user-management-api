from fastapi import FastAPI
# from config.settings import settings
# from models.user_model import User
# from config.db import db
# import bcrypt
from routers.user_router import userRouter

app = FastAPI()


app.include_router(userRouter, prefix="/api/users")
