from random import randint
from db import db
from sqlalchemy.sql import text


def login(username):

    sql = text("SELECT id,isAdmin, password FROM USERS WHERE username=:username")
    result = db.session.execute(sql, {"username": username}).fetchone()
    return result


def create(username, password, is_admin):

    sql = text("""
        INSERT INTO USERS (username, password, isAdmin)
        VALUES (:username, :password, :isAdmin)
        RETURNING username
    """)
    db.session.execute(sql,
                       {"username": username,
                        "password": password,
                        "isAdmin": is_admin})
    db.session.commit()


def favourites(id):

    sql = text("""
            SELECT
              fav.userFriended_id,
              us.username
             FROM
             users us
            RIGHT JOIN
              favorites fav
            ON
              fav.userFriended_id= us.id

            WHERE
              fav.user_id=:id

             """)
    return db.session.execute(sql, {"id": id})
