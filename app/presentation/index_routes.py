from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.business.movie_service import *
from sqlalchemy.orm import joinedload
from app.data.models import Movie,  Comment
from app.data.models.genre import Genre
from app.data.models.actor import Actor
from app.business.comment_service import *
from flask_login import current_user, login_required
from app.presentation.form import CommentForm
from app.data.models.watch_history import WatchHistory
from datetime import datetime
from app.data.db_connection import db



bp = Blueprint("index",__name__, template_folder="templates")

@bp.route("/")
def index():
    pagination = get_movies_paginated_service()
    return render_template( "index.html", movies=pagination.items, pagination=pagination )

@bp.route("/genre/<int:genre_id>")
def by_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    pagination = get_movies_paginated_service("genre", genre_id)
    return render_template("movies/genre_list.html",
                           genre=genre,
                           movies=pagination.items,
                           pagination=pagination)

@bp.route("/actor/<int:actor_id>")
def by_actor(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    pagination = get_movies_paginated_service("actor", actor_id)
    return render_template("movies/actor_list.html",
                           actor=actor,
                           movies=pagination.items,
                           pagination=pagination)

@bp.route("/search")
def search():
    keyword = request.args.get("q", "").strip()
    pagination = None
    if keyword:
        pagination = get_movies_paginated_service("title", keyword)
    return render_template("movies/research_list.html", movies=pagination.items if pagination else [],
                           pagination=pagination, keyword=keyword)

@bp.route('/rank')
def rank():
    return render_template("rank.html")


@bp.route("/movies/<int:movie_id>", methods=["GET", "POST"])
def movie_detail(movie_id):
    # Tải phim và các bình luận liên quan
    movie = (Movie.query
             .options(joinedload(Movie.genres),
                      joinedload(Movie.comments).joinedload(Comment.account))
             .get_or_404(movie_id))

    form = CommentForm()

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('Bạn phải đăng nhập để bình luận.', 'danger')
            return redirect(url_for('user.auth_user'))

        add_comment(current_user.id, movie.id, form.content.data)
        flash('Bình luận của bạn đã được gửi!', 'success')
        return redirect(url_for('index.movie_detail', movie_id=movie_id))

    return render_template("movies/movie_detail.html", movie=movie, form=form)


# Route để sửa bình luận
@bp.route("/comments/<int:comment_id>/edit", methods=["POST"])
@login_required
def edit_comment_route(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.account_id != current_user.id:
        flash("Bạn không có quyền sửa bình luận này.", "danger")
        return redirect(url_for('index.movie_detail', movie_id=comment.movie_id))

    new_review = request.form.get("new_review")
    if new_review:
        update_comment(comment_id, new_review)
        flash("Bình luận đã được cập nhật.", "success")
    return redirect(url_for('index.movie_detail', movie_id=comment.movie_id))


# Route để xóa bình luận
@bp.route("/comments/<int:comment_id>/delete", methods=["POST"])
@login_required
def delete_comment_route(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.account_id != current_user.id:
        flash("Bạn không có quyền xóa bình luận này.", "danger")
        return redirect(url_for('index.movie_detail', movie_id=comment.movie_id))

    delete_comment(comment_id)
    flash("Bình luận đã được xóa.", "success")
    return redirect(url_for('index.movie_detail', movie_id=comment.movie_id))

@bp.route("/watch/<int:episode_id>", methods=["POST"])
@login_required
def watch_episode(episode_id):
    from datetime import datetime
    from flask import request
    from app.data.models.episode import Episode

    episode = Episode.query.get_or_404(episode_id)
    data = request.get_json(silent=True) or {}
    progress_seconds = data.get("progress", 0)  # nhận progress (giây)

    existing = WatchHistory.query.filter_by(
        account_id=current_user.id,
        episode_id=episode.id
    ).first()

    if existing:
        existing.progress = progress_seconds
        existing.last_watched = datetime.now()
    else:
        db.session.add(WatchHistory(
            account_id=current_user.id,
            episode_id=episode.id,
            progress=progress_seconds,
            last_watched=datetime.now()
        ))

    db.session.commit()
    return {"status": "ok"}

