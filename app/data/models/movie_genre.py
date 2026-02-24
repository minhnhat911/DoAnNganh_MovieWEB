from app.data.db_connection import db

movie_genre = db.Table(
    "movie_genre",
    db.Column("movie_id", db.Integer, db.ForeignKey("movies.id"), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genres.id"), primary_key=True)
)