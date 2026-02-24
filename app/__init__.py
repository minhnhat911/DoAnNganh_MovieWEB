from flask import Flask
from app.config import Config
from app.data.db_connection import *
from app.presentation import index_routes, admin
from app.presentation.admin import init_admin
from app.presentation.user_routes import user_bp
from flask_login import LoginManager
from app.data.models.genre import Genre
import cloudinary


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Khởi tạo DB
    db.init_app(app)
    login.init_app(app)

    app.register_blueprint(index_routes.bp)
    app.register_blueprint(user_bp)

    init_admin(app)
    @app.context_processor
    def inject_nav_genres():
        genres = Genre.query.order_by(Genre.name.asc()).all()
        return {"nav_genres": genres}

    cloudinary.config(
        cloud_name="dxavze1c0",
        api_key="511362823432556",
        api_secret="z5LGI05-G5b-gQD1T9R5Xq0YVyQ",
        secure=True
    )

    return app
