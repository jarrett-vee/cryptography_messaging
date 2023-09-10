from dotenv import load_dotenv

load_dotenv("setup.env")

from flask import Flask
from routes.keys import keys_bp


from extensions import Config, bcrypt, db, login_manager
from models import User
from routes.auth import auth_bp
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "auth.login"
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(keys_bp, url_prefix="/keys")
migrate = Migrate(app, db)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == "__main__":
    app.run(debug=True)
