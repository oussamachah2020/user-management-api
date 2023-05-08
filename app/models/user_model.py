from pydantic import BaseModel, EmailStr, Field
import uuid

class registrationModel(BaseModel):
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


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message
    }

def ErrorResponse(error, code, message):
    return {"error": error, "code": code, "message": message}


class loginModel(BaseModel):
    email: str = Field(...)
    password: str = Field(...)
