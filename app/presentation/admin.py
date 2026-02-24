# admin.py

from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.model.template import EndpointLinkRowAction
from flask import request
from flask_login import current_user, login_required
from datetime import datetime
from sqlalchemy import text


# Import các model và session từ các file của bạn
from app.data.models.actor import Actor
from app.data.models.genre import Genre
from app.data.models.watch_history import WatchHistory
from app.data.models.movie import Movie
from app.data.models.episode import Episode
from app.data.db_connection import db
from app.data.models.account import Account
from app.data.models.user import User
from app.data.models.base import BaseModel


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        # Yêu cầu người dùng phải đăng nhập và có vai trò Admin để truy cập
        return current_user.is_authenticated and current_user.role.name == 'Admin'

    @expose('/')
    def index(self, **kwargs):
        period = request.args.get('period', 'month')
        current_year = datetime.now().year
        current_month = datetime.now().month

        month = request.args.get('month', type=int)
        year = request.args.get('year', type=int)

        if not month:
            month = current_month
        if not year:
            year = current_year

        rows = []
        labels = []
        values = []

        try:
            result = db.session.execute(
                text("CALL get_top_10_movies_by_views(:period, :month, :year)"),
                {"period": period, "month": month, "year": year}
            )
            rows = result.fetchall()

            for row in rows:
                labels.append(row.title)
                values.append(row.total_views)

        except Exception as e:
            # Xử lý ngoại lệ nếu có lỗi khi gọi stored procedure
            print(f"Lỗi khi gọi stored procedure: {e}")

        return self.render('admin/dashboard.html',
                           period=period,
                           month=month,
                           year=year,
                           rows=rows,
                           labels=labels,
                           values=values)


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.name == 'Admin'

class GenreView(AuthenticatedModelView):
    column_list = ["name"]
    form_columns = ["name"]

class ActorView(AuthenticatedModelView):
    column_list = ["name", "date_of_birth"]

class WatchHistoryView(AuthenticatedModelView):
    column_list = ["account_id", "episode", "progress", "last_watched"]
    form_columns = ["account_id", "episode", "progress", "last_watched"]


class UserView(AuthenticatedModelView):
    column_list = ['first_name', 'last_name', 'date_of_birth']
    form_columns = ['first_name', 'last_name', 'gender', 'date_of_birth', 'email', 'phone']

class AccountView(AuthenticatedModelView):
    column_list = ['id', 'username', 'role', 'is_active', 'is_pro', 'user', 'last_login', 'avatar_url']
    form_columns = ['username', 'password', 'role', 'is_active', 'is_pro', 'avatar_url', 'user']

class MovieView(AuthenticatedModelView):
    column_list = ["title", "release_year", "rating", "genres", "actors"]
    form_columns = ["title", "description", "release_year", "duration",
                    "rating", "poster_url", "trailer_url", "genres", "actors", "is_pro"]

    column_extra_row_actions = [
        # List tập phim
        EndpointLinkRowAction(
            'fa fa-film',
            'episode.index_view',
            id_arg='movie_id'
        )
    ]

class EpisodeView(AuthenticatedModelView):
    column_list = ('title', 'movie', 'episode_number')

    # Ghi đè phương thức get_query để lọc dữ liệu
    def get_query(self):
        query = super(EpisodeView, self).get_query()
        movie_id = request.args.get('movie_id')
        if movie_id:
            query = query.filter(Episode.movie_id == movie_id)

        return query

    def get_count_query(self):
        query = super(EpisodeView, self).get_count_query()
        movie_id = request.args.get('movie_id')
        if movie_id:
            query = query.filter(Episode.movie_id == movie_id)

        return query

def init_admin(app):
    admin = Admin(app, name="Trang Quản Trị ViewLife+", template_mode="bootstrap4", index_view=MyAdminIndexView())

    admin.add_view(MovieView(Movie, db.session))
    admin.add_view(GenreView(Genre, db.session))
    admin.add_view(ActorView(Actor, db.session))
    admin.add_view(WatchHistoryView(WatchHistory, db.session))
    admin.add_view(EpisodeView(Episode, db.session))

    admin.add_view(UserView(User, db.session, endpoint="admin_users"))
    admin.add_view(AccountView(Account, db.session))
    return admin
