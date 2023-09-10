import pyotp
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from extensions import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    enable_2fa = db.Column(db.Boolean, default=False)
    secret_key = db.Column(db.String(16))
    public_key = db.Column(db.Text, nullable=True)
    encrypted_private_key = db.Column(db.LargeBinary, nullable=True)
