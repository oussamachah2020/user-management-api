from fastapi import FastAPI
from routers.user_router import userRouter

app = FastAPI()

app.include_router(userRouter, prefix="/api/users", tags=["Auth"])
