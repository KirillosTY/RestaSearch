from random import randint
from db import db
from sqlalchemy.sql import text


def login(username):

    sql = text("SELECT id,is_admin, password FROM USERS WHERE username=:username")
    result = db.session.execute(sql, {"username": username}).fetchone()
    return result


def create(username, password, is_admin):

    sql = text("""
        INSERT INTO USERS (username, password, is_admin)
        VALUES (:username, :password, :is_admin)
        RETURNING username
    """)
    db.session.execute(sql,
                       {"username": username,
                        "password": password,
                        "is_admin": is_admin})
    db.session.commit()


def favourites(id):

    sql = text("""
            SELECT
              fav.user_friended_id,
              us.username
             FROM
             users us
            RIGHT JOIN
              favorites fav
            ON
              fav.user_friended_id= us.id

            WHERE
              fav.user_id=:id

             """)
    return db.session.execute(sql, {"id": id})
