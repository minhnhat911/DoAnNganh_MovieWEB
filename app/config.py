import os
from urllib.parse import quote


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret-key-demo"

    # DB_USER = os.environ.get("DB_USER", "root")
    # DB_PASSWORD = quote(os.environ.get("DB_PASSWORD", "Admin@123"))
    # DB_NAME = os.environ.get("DB_NAME", "bookstore")
    # DB_HOST = os.environ.get("DB_HOST", "localhost")

    # Kết nối MySQL qua PyMySQL
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:%s@localhost/movieweb_db?charset=utf8mb4" % quote("Admin@123")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PAGE_SIZE = 4
