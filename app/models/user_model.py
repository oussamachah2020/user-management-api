from pydantic import BaseModel
from bson import objectid


class registrationModel(BaseModel):
    _id: objectid
    username: str
    email: str
    password: str


class loginModel(BaseModel):
    _id: objectid
    email: str
    password: str
