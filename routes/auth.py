from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    session,
    jsonify,
)
from models import User, db
from extensions import bcrypt
import pyotp
from flask_login import login_user, logout_user, current_user, login_required
import time

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        enable_2fa = request.form.get("enable_2fa") == "on"

        # Check if the username already exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username is already taken. Please choose another one.")
            return render_template("register.html")

        if enable_2fa:
            secret_key = pyotp.random_base32()
            print(secret_key)
        else:
            secret_key = None

        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

        new_user = User(
            username=username,
            password_hash=password_hash,
            enable_2fa=enable_2fa,
            secret_key=secret_key,
        )

        db.session.add(new_user)
        db.session.commit()

        if enable_2fa:
            flash("Please set up 2FA using the provided secret.")
            return redirect(url_for("auth.setup_2fa", secret_key=secret_key))

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/setup_2fa/<secret_key>", methods=["GET", "POST"])
def setup_2fa(secret_key):
    if request.method == "POST":
        user_input_otp = request.form.get("otp")
        if pyotp.TOTP(secret_key).verify(user_input_otp):
            flash("2FA set up successfully")
            return redirect(url_for("auth.login"))
        flash("Invalid OTP. Please try again")
    otp_uri = pyotp.totp.TOTP(secret_key).provisioning_uri(
        name="ChatBot", issuer_name="ChatBotInc."
    )

    return render_template("setup_2fa.html", otp_uri=otp_uri)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("keys.get_public_key"))

    if request.method == "POST":
        if session.get("login_attempts", 0) >= 3:
            if time.time() - session.get("last_attempt_time", 0) < 300:
                return "Too many failed attempts. Please wait."

            session["login_attempts"] = 0

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            session["login_attempts"] = 0
            if user.enable_2fa:
                return redirect(url_for("auth.verify_2fa"))
            else:
                flash("Login successful!", "success")
                return redirect(
                    url_for("keys.get_public_key")
                )  # redirect to the get_public_key route after login
        else:
            session["login_attempts"] = session.get("login_attempts", 0) + 1
            session["last_attempt_time"] = time.time()
            return jsonify(success=False, error_message="Invalid username or password")

    return render_template("login.html")


@auth_bp.route("/verify_2fa", methods=["GET", "POST"])
def verify_2fa():
    if "2fa_user_id" not in session:
        return redirect(url_for("auth.login"))

    user = User.query.get(session["2fa_user_id"])

    if request.method == "POST":
        user_input_otp = request.form.get("otp")
        if pyotp.TOTP(user.secret_key).verify(user_input_otp):
            del session["2fa_user_id"]
            session["user_id"] = user.id
            flash("Logged in successfully")
            return redirect("/")  # Redirect to the user dashboard or main page
        flash("Invalid OTP. Please try again")
    return render_template("verify_2fa.html")
