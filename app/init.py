from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager

myapp = Flask(__name__)

myapp.secret_key = "ui21eui2g"

myapp.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:mysql@localhost/ql_maybay?charset=utf8mb4"
myapp.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=myapp)

admin = Admin(app=myapp, name="Quan Ly Ve May Bay", template_mode="bootstrap3")

login = LoginManager(app=myapp)