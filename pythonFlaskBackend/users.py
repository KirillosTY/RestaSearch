import os
import user_db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import secrets


def jsonifyUser(username, rawData):
    user_data = {
        "id": rawData[0],
        "is_admin": rawData[1],
        "password": rawData[2],
        "username": username
    }
    return user_data


def login(username, password):
    result = user_db.login(username)

    if result is None:
        return None

    user = jsonifyUser(username, result)

    if check_password_hash(user.get("password"), password):
        print(user.get('is_admin'), 'here')
        userSessionSetup(user)

        return True
    else:
        return False


def getFavouriteFriends(id):
    result = user_db.favourites(id)
    return result.fetchall()


def create(username, password, is_admin):

    hash_password = generate_password_hash(password)
    try:
        user_db.create(username, hash_password, is_admin)

    except BaseException:
        return False

    return login(username, password)
  

def checkSession():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)


def is_admin():
    if session["is_admin"] != request.form["True"]:
        abort(403)


def userSessionSetup(user):

    session["user"] = user.get("username")
    session["user_id"] = user.get("id")
    session["is_admin"] = user.get("is_admin")
    session["csrf_token"] = secrets.token_hex(16)


def delete_session():
    del session["user"]
    del session["user_id"]
    del session["is_admin"]
    del session["csrf_token"]


def check_csrf():
    print(session["csrf_token"],  request.form["csrf_token"])
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
