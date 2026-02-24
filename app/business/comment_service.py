from app.data.repositories import comment_dao


def add_comment(account_id, movie_id, review):

    if not review or not review.strip():
        raise ValueError("Nội dung bình luận không được rỗng")
    return comment_dao.add_comment(account_id, movie_id, review.strip())


def get_comments_by_movie(movie_id):
    return comment_dao.get_comments_by_movie(movie_id)


def get_comment_by_id(comment_id):
    return comment_dao.get_comment_by_id(comment_id)


def update_comment(comment_id, new_review):
    if not new_review or not new_review.strip():
        raise ValueError("Nội dung bình luận không được rỗng")

    return comment_dao.update_comment(comment_id, new_review.strip())


def delete_comment(comment_id):
    return comment_dao.delete_comment(comment_id)

