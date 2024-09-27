from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager

from .config import Config

bcrypt= Bcrypt()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    login_manager.login_view = "user_bp.login"

    from .routes import init_routes
    init_routes(app)

    bcrypt.init_app(app)

    with app.app_context():
        db.create_all()

    return app