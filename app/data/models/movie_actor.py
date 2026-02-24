from app.data.db_connection import db

movie_actor = db.Table(
    "movie_actor",
    db.Column("movie_id", db.Integer, db.ForeignKey("movies.id"), primary_key=True),
    db.Column("actor_id", db.Integer, db.ForeignKey("actors.id"), primary_key=True)
)