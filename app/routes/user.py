from flask import Blueprint, request, jsonify
from ..models import User
from .. import db, bcrypt

user_bp = Blueprint('user_bp',__name__)

@user_bp.route('/register', methods = ['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists."}), 400

    if username and password:
        hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username,password=hash_password)
        db.session.add(user)
        db.session.commit()
        return jsonify ({"message" : f"successful register for {username}"}),201
    return jsonify({"error":"couldn't register"}),400


@user_bp.route('/login', methods=["POST"])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username:
        user = User.query.filter_by(username=username).first()
        if bcrypt.check_password_hash(user.password,password):
            return jsonify({"message":f"successfully login as {username}"}), 201