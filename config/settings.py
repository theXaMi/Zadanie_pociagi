import os

SECRET_KEY = os.getenv("SECRET_KEY",None)
SERVER_NAME = os.getenv("SERVER_NAME",
                "localhost:{0}".format(os.getenv("DOCKER_WEB_PORT",
                                                    "8000")))

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL","redis://redis:6379/0")
RESULT_BACKEND = CELERY_BROKER_URL
CACHE_BACKEND = "memory"
ACCEPT_CONTENT = ["json"]
TASK_SERIALIZER = "json"
RESULT_SERIALIZER = "json"
REDIS_MAX_CONNECTIONS = 5

user = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]
host = os.environ["POSTGRES_HOST"]
database = os.environ["POSTGRES_DB"]
port = os.environ["POSTGRES_PORT"]

SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
SQLALCHEMY_TRACK_MODIFICATIONS = False