from app.data.models.comment import Comment
from app.data.db_connection import db


def add_comment(account_id, movie_id, review):
    new_comment = Comment(
        account_id=account_id,
        movie_id=movie_id,
        review=review
    )
    db.session.add(new_comment)
    db.session.commit()
    return new_comment

def get_comments_by_movie(movie_id):
    return db.session.query(Comment).filter_by(movie_id=movie_id).order_by(Comment.created_at.desc()).all()

def get_comment_by_id(comment_id):
    return db.session.query(Comment).get(comment_id)

def update_comment(comment_id, new_review):
    comment = get_comment_by_id(comment_id)
    if comment:
        comment.review = new_review
        db.session.commit()
        return True
    return False

def delete_comment(comment_id):
    comment = get_comment_by_id(comment_id)
    if comment:
        db.session.delete(comment)
        db.session.commit()
        return True
    return False