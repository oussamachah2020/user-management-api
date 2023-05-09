import datetime
import json
from fastapi import APIRouter, Response
from utils.response_util import response_msg
from config.settings import settings
from models.user_model import userModel, loginModel
from config.db import db
import bcrypt
import jwt
from bson import ObjectId

userRouter = APIRouter()

expires_at = datetime.datetime.utcnow() + datetime.timedelta(day=1)


@userRouter.post("/register", status_code=201)
async def create_user(user: userModel):
    existed_user = db.users.find_one({"email": user.email})

    if existed_user:
        return Response(status_code=409, content=response_msg("msg", "user already exists"))

    userDict = {
        "_id": str(ObjectId()),
        "username": user.username,
        "email": user.email,
        "password": user.password
    }

    if isinstance(userDict["password"], str):
        salt = bcrypt.gensalt(10)
        hashed_password = bcrypt.hashpw(
            userDict["password"].encode("utf-8"), salt)
        userDict["password"] = hashed_password.decode("utf-8")

    if userDict:
        db.users.insert_one(userDict)
        encoded_jwt = jwt.encode(
            {userDict["_id"]: "payload"}, settings.JWT_PRIVATE_KEY, algorithm="HS256")
        print(encoded_jwt)
        return Response(status_code=201, content=response_msg("msg", "user created successfully"))


@userRouter.post("/login", status_code=200)
async def get_user(user: loginModel):
    try:
        auth_user = db.users.find_one({"email": user.email})

        auth_user_dict = dict(auth_user)

        if auth_user is None:
            return Response(status_code=404, content=response_msg("msg", "user not found"))
        else:
            encoded_password = user.password.encode("utf-8")
            password_to_check = auth_user_dict['password']
            if isinstance(password_to_check, str):
                password_to_check = password_to_check.encode("utf-8")
                password_matching = bcrypt.checkpw(
                    encoded_password, password_to_check)
                if password_matching:
                    encoded_jwt = jwt.encode(
                        {auth_user_dict["_id"]: "payload", "exp": expires_at}, settings.JWT_PRIVATE_KEY, algorithm="HS256")

                    return Response(status_code=200, content=response_msg("token", encoded_jwt))
                else:
                    return Response(status_code=400, content=response_msg("msg", "incorrect password"))
    except Exception as e:
        return Response(status_code=500, content=response_msg("error", e))


@userRouter.put("/update_user")
async def update_user(user: userModel):
    target_user = db.users.find_one_and_update({"_id": user.id})
