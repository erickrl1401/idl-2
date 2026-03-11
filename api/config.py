import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Database
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "gestion_clientes")

    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-secret-in-production")
    JWT_ACCESS_TOKEN_EXPIRES_HOURS = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_HOURS", 8))

    # Flask
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    PORT = int(os.getenv("FLASK_PORT", 5000))
