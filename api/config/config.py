import os
from decouple import config
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = config("DATABASE_URL")



class DevConfig(Config):
    SQLALCHEMY_ECHO= True
    Debug = True
    secret_key= os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

class ProdConfig(Config):
    pass

class TestConfig(Config):
    pass

config_dict ={
    'dev' : DevConfig,
    'prod' : ProdConfig,
    'test' : TestConfig,
}