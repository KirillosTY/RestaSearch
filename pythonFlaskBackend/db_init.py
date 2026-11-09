from app import app
from db import db
import user_db
from werkzeug.security import generate_password_hash

@app.cli.command("init-db")
def create_db():
    with app.open_resource("schemas/Start.sql", "r") as f:
        sql_start = f.read()
        connection = db.engine.raw_connection()
        connection.executescript(sql_start)
        connection.close()
        user_db.create("testadmin",generate_password_hash("Testing123"), True)

        print("creating database and admin was successful, probably.\n")
      