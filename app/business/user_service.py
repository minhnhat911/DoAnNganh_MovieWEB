from app.data.repositories.user_dao import *

class UserService:

    def add_user(first_name, last_name, username, password, avatar_url=None, email=None):

        # Thêm vào DB
        user = UserDAO.add_user(first_name,last_name, username, password,avatar_url, email)
        return {"success": True, "message": "Đăng ký thành công!", "user": user}

    def auth_user(username, password, role=None):

        return UserDAO.auth_user(username, password, role)

    def get_account_by_id(account_id):
        return UserDAO.get_account_by_id(account_id)