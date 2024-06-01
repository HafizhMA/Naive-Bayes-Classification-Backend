from flask import Blueprint, jsonify, request
from models.model import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
import datetime

registerlogin = Blueprint('registerlogin', __name__, template_folder='routes')

@registerlogin.route('/register', methods=['POST'])
def register_data():
    db.create_all()
    data = request.get_json()
    nama = data.get('nama')
    password = data.get('password')

    if not nama or not password:
        return jsonify({'message': 'Nama dan password diperlukan'}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(nama=nama, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@registerlogin.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    nama = data.get('nama')
    password = data.get('password')

    user = User.query.filter_by(nama=nama).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Nama atau password salah'}), 401

    access_token = create_access_token(identity={'id': user.id, 'nama': user.nama}, expires_delta=datetime.timedelta(hours=1))
    return jsonify(access_token=access_token), 200