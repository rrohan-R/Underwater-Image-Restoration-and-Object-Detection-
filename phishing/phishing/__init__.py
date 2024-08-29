from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import FlaskForm,CSRFProtect
from flask_mail import Mail



import torch
import torch.backends.cudnn as cudnn

app = Flask(__name__)

UPLOAD_FOLDER = 'phishing/static/uploads'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

app.config['SECRET_KEY'] = '8ea2a86e42689205dde0ba81f31138b6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phishing.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app) 

from phishing import routes

    
app.app_context().push()