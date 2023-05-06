from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: str
    JWT_PRIVATE_KEY: str
    JWT_PRIVATE_KEY: str

    class Config:
        env_file = '../.env'


settings = Settings()
