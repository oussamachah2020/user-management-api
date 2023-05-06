from fastapi import APIRouter, Response
from config.settings import settings
from models.user_model import registrationModel, loginModel
from config.db import db
import bcrypt
import jwt

userRouter = APIRouter()


@userRouter.post("/create")
async def create_user(user: registrationModel):
    existed_user = db.users.find_one({"email": user.email})

    if existed_user:
        return Response(status_code=403, content="User already exists")

    encoded_password = user.password.encode('utf-8')
    salt = bcrypt.gensalt(10)
    hashed_password = bcrypt.hashpw(encoded_password, salt)
    user.password = hashed_password.decode('utf-8')

    newUser = db.users.insert_one(user.dict())

    encoded_jwt = jwt.encode({newUser._id: "payload"},
                             "secret", algorithm="HS256")

    if newUser:
        return Response(status_code=201, content=["user created successfully", {"token": encoded_jwt}])
    else:
        return Response(status_code=500)


@userRouter.get("/all")
async def get_user(user: loginModel):
    searched_user = db.users.find({"email": user.email})
    # user = searched_user.
    encoded_jwt = jwt.encode({user._id: "payload"},
                             settings.JWT_PRIVATE_KEY, algorithm="HS256")

    user_password_encoded = user.password.encode("utf-8")
    passwords_matching = bcrypt.checkpw(
        user_password_encoded, searched_user.password)

    if searched_user:
        if passwords_matching:
            return Response(status_code=200, content={"token": encoded_jwt})
        else:
            return Response(status_code=400, content="Incorrect password")
    else:
        return Response(status_code=404, content="user not found")
