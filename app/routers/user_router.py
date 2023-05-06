from fastapi import APIRouter, Response
from config.settings import settings
from models.user_model import User
from config.db import db
import bcrypt

userRouter = APIRouter()


@userRouter.post("/create")
async def create_user(user: User):
    existed_user = db.users.find_one({"email": user.email})

    if existed_user:
        return Response(status_code=403, content="User already exists")

    encoded_password = user.password.encode('utf-8')
    salt = bcrypt.gensalt(10)
    hashed_password = bcrypt.hashpw(encoded_password, salt)
    user.password = hashed_password.decode('utf-8')

    newUser = db.users.insert_one(user.dict())

    if newUser:
        return Response(status_code=201, content=["user created successfully", {"user": user}])
    else:
        return Response(status_code=500)
