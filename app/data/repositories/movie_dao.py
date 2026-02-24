from flask import request
from app.data.models.movie import Movie
from app.data.models.watch_history import WatchHistory
from datetime import datetime
from app.data.db_connection import db

def get_movies_paginated(filter_type=None, filter_value=None, page=None, per_page=20):
    """
    Trả về danh sách phim phân trang, lọc theo:
      - genre_id
      - actor_id
      - title (search keyword)
    """
    if page is None:
        page = request.args.get("page", 1, type=int)
    if per_page is None:
        per_page = request.args.get("per_page", 20, type=int)

    query = Movie.query

    if filter_type == "genre":
        query = query.filter(Movie.genres.any(id=filter_value))
    elif filter_type == "actor":
        query = query.filter(Movie.actors.any(id=filter_value))
    elif filter_type == "title":
        # LIKE cho MySQL (ilike nếu DB hỗ trợ)
        query = query.filter(Movie.title.ilike(f"%{filter_value}%"))

    return query.order_by(Movie.created_at.desc()) \
                .paginate(page=page, per_page=per_page, error_out=False)

