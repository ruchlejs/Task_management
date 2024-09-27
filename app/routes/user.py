from flask import Blueprint, request, jsonify, redirect
from ..models import User
from .. import db, bcrypt, login_manager
from flask_login import login_user, logout_user, login_required

user_bp = Blueprint('user_bp',__name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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


@user_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if username:
            user = User.query.filter_by(username=username).first()
            if bcrypt.check_password_hash(user.password,password):
                next = request.args.get('next')
                login_user(user)
                if next:
                    redirect(next)
                return jsonify({"message":f"successfully login as {username}"}), 201
    else:
        return jsonify({"message": "Please provide your credentials."}), 200

        
@user_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message":"sucessfully logout"}), 201
