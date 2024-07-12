from flask import Flask
from forms import RegisterF, LoginF
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config["SECRET_KEY"] = "lukalukuna"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lukas.db"
db = SQLAlchemy(app)

login_manager = LoginManager(app)