from flask import Blueprint, jsonify, request
from models.model import db, User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
import datetime

registerlogin = Blueprint('registerlogin', __name__, template_folder='routes')

bcrypt = Bcrypt()

@registerlogin.route('/register', methods=['POST'])
def register_data():
    db.create_all()
    data = request.get_json()
    nama = data.get('nama')
    password = data.get('password')

    if not nama or not password:
        return jsonify({'message': 'Nama dan password diperlukan', 'status': 'fail'}), 400

    if User.query.filter_by(nama=nama).first():
        return jsonify({'message': 'Nama sudah digunakan', 'status': 'fail'}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(nama=nama, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    response = {
        'message': 'User berhasil dibuat',
        'status': 'success',
        'data': {
            'id': new_user.id,
            'nama': new_user.nama
        }
    }

    return jsonify(response), 201

@registerlogin.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    nama = data.get('nama')
    password = data.get('password')

    if not nama or not password:
        return jsonify({'message': 'Nama dan password diperlukan', 'status': 'fail'}), 400

    user = User.query.filter_by(nama=nama).first()

    if not user:
        return jsonify({'message': 'User tidak ditemukan', 'status': 'fail'}), 404

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': 'Password salah', 'status': 'fail'}), 401

    access_token = create_access_token(identity={'id': user.id, 'nama': user.nama}, expires_delta=datetime.timedelta(hours=1))
    
    response = {
        'message': 'Login berhasil',
        'status': 'success',
        'data': {
            'id': user.id,
            'token': access_token
        }
    }
    
    return jsonify(response), 200