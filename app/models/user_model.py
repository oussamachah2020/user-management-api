from pydantic import BaseModel, EmailStr, Field
import uuid


class userModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "example",
                "email": "example@example.com",
                "password": "password"
            }
        }


class responseModel(BaseModel):
    access_token: str
    refresh_token: str


def ErrorResponse(error, code, message):
    return {"error": error, "code": code, "message": message}


class loginModel(BaseModel):
    email: str = Field(...)
    password: str = Field(...)


class tokenModel(BaseModel):
    token: str = Field(...)
