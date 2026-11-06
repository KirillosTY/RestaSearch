from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event
from os import getenv
from app import app

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("dburl")

db = SQLAlchemy(app)




@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, _):
   
 

    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

 