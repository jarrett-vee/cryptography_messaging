from dotenv import load_dotenv

load_dotenv("setup.env")

from flask import Flask, render_template
from flask_cors import CORS
from routes.keys import keys_bp
from config import Config, db, login_manager
from models import User, Message
from routes.auth import auth_bp
from flask_migrate import Migrate
from flask_login import login_required, current_user
from routes.messages import messages_bp


app = Flask(__name__)
app.config.from_object(Config)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
CORS(app)
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "auth.login"
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(keys_bp, url_prefix="/keys")
app.register_blueprint(messages_bp, url_prefix="/messages")
migrate = Migrate(app, db)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/dashboard")
@login_required
def dashboard():
    sent_messages = Message.query.filter_by(sender_id=current_user.id).all()
    received_messages = Message.query.filter_by(receiver_id=current_user.id).all()
    return render_template(
        "dashboard.html",
        sent_messages=sent_messages,
        received_messages=received_messages,
    )


if __name__ == "__main__":
    app.run(debug=True)
