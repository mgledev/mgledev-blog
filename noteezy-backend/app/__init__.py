from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
CORS(app)

app.config.from_envvar("FLASK_CONFIG", silent=True)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///noteezy.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

limiter = Limiter(get_remote_address, app=app)

from app import routes, models