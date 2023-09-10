from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import User
from flask_login import login_required

keys_bp = Blueprint("keys", __name__)


@keys_bp.route("/get_public_key", methods=["GET", "POST"])
@login_required
def get_public_key():
    if request.method == "POST":
        username = request.form.get("username")
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template("display_key.html", public_key=user.public_key)
        else:
            flash("User not found!", "danger")

    return render_template("get_public_key.html")
