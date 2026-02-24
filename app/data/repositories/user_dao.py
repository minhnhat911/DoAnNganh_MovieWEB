from datetime import datetime
from app.data.db_connection import db
from app.data.models import Account, User

import hashlib

class UserDAO:

    def add_user(first_name, last_name, username, password, avatar_url=None, email=None):
        password = str(hashlib.md5(password.encode("utf-8")).hexdigest())

        # 1. Tạo record User
        user = User(
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            email=email.strip() if email else None
        )
        db.session.add(user)
        db.session.flush()  # để lấy user.id ngay lập tức

        # 2. Tạo record Account liên kết với User
        account = Account(
            username=username.strip(),
            password=password,
            user_id=user.id,
            avatar_url=avatar_url
        )
        db.session.add(account)
        db.session.commit()
        return user, account

    def auth_user(username, password, role=None):
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        account = Account.query.filter(
            Account.username == username,
            Account.password == password
        ).first()

        if account:
            # cập nhật last_login ngay khi đăng nhập thành công
            account.last_login = datetime.now()
            db.session.commit()
        return account

    def get_account_by_id(account_id):
        return Account.query.get(account_id)
