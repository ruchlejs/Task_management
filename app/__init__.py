from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from .config import Config

bcrypt= Bcrypt()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from .routes import init_routes
    init_routes(app)

    bcrypt.init_app(app)

    with app.app_context():
        db.create_all()

    return app