from flask import Flask
from flask_bootstrap import Bootstrap5


from os import getenv


app = Flask(__name__)
bootstrap = Bootstrap5(app)

app.secret_key = getenv("SECRET")
import routes

