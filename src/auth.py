from flask import Blueprint, jsonify, request
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def signup_post():
    json_data = request.get_json(force=True)
    email = json_data['email']
    username = json_data['username']
    password = json_data['password']
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify(['El usuario ya existe']), 409
    
    new_user = User(email=email, name=username, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(['Usuario creado con éxito']), 201

@auth.route('/login', methods=['POST'])
def login_post():
    json_data = request.get_json(force=True)
    email = json_data['email']
    password = json_data['password']
    remember = True if json_data['remember'] else False
    
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify(['Contraseña o usuario incorrectos'])
    login_user(user, remember=remember)
    
    return jsonify(['Éxito', user.name])