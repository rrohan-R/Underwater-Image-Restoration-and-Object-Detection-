from email.policy import default
from enum import unique
from ssl import _create_unverified_context
from phishing import db,app,login_manager
from flask_login import UserMixin
from flask_table import Table, Col, LinkCol
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship 


@login_manager.user_loader
def load_user(id):
    return Register.query.get(int(id))




class Register(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(200))
    contact= db.Column(db.String(200))
  

