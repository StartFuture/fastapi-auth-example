import os
from dotenv import load_dotenv

load_dotenv()

DB_PG_HOST = os.environ.get("DB_PG_HOST")
DB_PG_PORT = os.environ.get("DB_PG_PORT")
DB_PG_DATABASE = os.environ.get("DB_PG_DATABASE")
DB_PG_USERNAME = os.environ.get("DB_PG_USERNAME")
DB_PG_PASSWORD = os.environ.get("DB_PG_PASSWORD")
DB_PG_SCHEMA = os.environ.get("DB_PG_SCHEMA")

APP_MODE = os.environ.get("APP_MODE")

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE = os.environ.get("ACCESS_TOKEN_EXPIRE")

EMAIL_NAME = os.environ.get("EMAIL_NAME")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

HOST_FRONT = os.environ.get("HOST_FRONT")
SUPPORT_URL = f'{os.environ.get("HOST_FRONT")}/support'

APP_MODE_DEV = 'dev'