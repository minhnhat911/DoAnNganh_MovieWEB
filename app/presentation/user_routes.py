from flask import Blueprint, render_template, request,redirect, url_for, session
from app.business.user_service import *
from app.data.db_connection import *

from flask_login import login_user, logout_user
import cloudinary.uploader

user_bp = Blueprint("user", __name__, template_folder="templates/users")


@user_bp.route("/register", methods=["GET", "POST"])
def add_user():
    err_msg = ""
    if request.method.__eq__("POST"):
        first_name = request.form.get("name")
        last_name = request.form.get("last-name")
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        confirm = request.form.get("password_confirmation")
        avatar_url = None
        try:
            if password.strip() == confirm.strip():
                avatar = request.files.get("avatar")
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_url = res["secure_url"]

                UserService.add_user(
                    first_name=first_name,
                    last_name = last_name,
                    username=username,
                    password=password,
                    email=email,
                    avatar_url = avatar_url
                )
                return redirect(url_for("user.auth_user"))  # chuyển về trang chủ
            else:
                err_msg = "Mật khẩu KHÔNG khớp!!!"
        except Exception as ex:
            err_msg = "Hệ thống đang có lỗi: " + str(ex)

    return render_template("users/register.html", err_msg=err_msg)


@user_bp.route('/login', methods=["GET", "POST"])
def auth_user():
    err_msg = ""
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        acc = UserService.auth_user(username=username, password=password)
        if acc:
            login_user(user=acc)
            return redirect(url_for('index.index'))
        else:
            err_msg = "Something wrong!!!"

    return render_template("login.html", err_msg=err_msg)

@login.user_loader
def user_load(account_id):
    return UserService.get_account_by_id(account_id=account_id)

@user_bp.route("/user-logout")
def user_signout():
    logout_user()
    return redirect(url_for("user.auth_user"))