from flask import Flask
from flask_bootstrap import Bootstrap5
import logging
from os import getenv

app = Flask(__name__)
bootstrap = Bootstrap5(app)
# #Flaw 5
# app.logger.setLevel(logging.WARNING)
# log_file = logging.FileHandler("security.log")
# log_file.setLevel(logging.WARNING)
# log_file.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s %(funcName)s"))
# app.logger.addHandler(log_file) 
app.secret_key = getenv("SECRET")
import routes
import db_init
