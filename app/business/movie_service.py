from app.data.repositories import movie_dao

def get_movies_paginated_service(filter_type=None, filter_value=None, page=None, per_page=20):
    return movie_dao.get_movies_paginated(
        filter_type=filter_type,
        filter_value=filter_value,
        page=page,
        per_page=per_page
    )