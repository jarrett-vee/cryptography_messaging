from flask_login import UserMixin
from config import db
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    enable_2fa = db.Column(db.Boolean, default=False)
    secret_key = db.Column(db.String(16))
    public_key = db.Column(db.String, nullable=True)
    encrypted_private_key = db.Column(db.LargeBinary, nullable=True)
    sent_messages = db.relationship(
        "Message", backref="sender", foreign_keys="Message.sender_id"
    )
    received_messages = db.relationship(
        "Message", backref="receiver", foreign_keys="Message.receiver_id"
    )


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    receiver_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    encrypted_message = db.Column(db.LargeBinary, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
