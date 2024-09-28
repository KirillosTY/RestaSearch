from random import randint
from db import db
from sqlalchemy.sql import text


def login(username):

  sql = text("SELECT id,isAdmin, password FROM USERS WHERE username=:username")
  return db.session.execute(sql, {"username":username})

def create(username,password,isAdmin):

    sql = text("""
        INSERT INTO USERS (username, password, isAdmin)
        VALUES (:username, :password, :isAdmin)
    """)
    db.session.execute(sql, {"username": username, "password": password, "isAdmin": isAdmin})
    db.session.commit()
 