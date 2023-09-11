from flask import Blueprint, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models import Message, User
from config import db

messages_bp = Blueprint("messages", __name__)


@messages_bp.route("/send", methods=["POST"])
@login_required
def send_message():
    data = request.form
    receiver_username = data.get("receiver_username")
    encrypted_message = data.get("encrypted_message")

    encrypted_message_bytes = encrypted_message.encode("utf-8")

    receiver = User.query.filter_by(username=receiver_username).first()
    if not receiver:
        return jsonify({"error": "Receiver not found!"}), 404

    message = Message(
        sender_id=current_user.id,
        receiver_id=receiver.id,
        encrypted_message=encrypted_message_bytes,  # Use the bytes version
    )

    db.session.add(message)
    db.session.commit()

    flash("Message sent successfully!")
    return redirect(url_for("dashboard"))
