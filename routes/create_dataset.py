from flask import Blueprint, jsonify, request
import pandas as pd
from function.obj_converter import call_dataset_obj
from main import db
from models.model import Dataset
import os
from collections import Counter

create_dataset = Blueprint('create_dataset', __name__, template_folder='routes')

UPLOAD_FOLDER = 'dataset'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@create_dataset.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return {'error': 'No file part'}, 400
    file = request.files['file']
    if file.filename == '':
        return {'error': 'No selected file'}, 400
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        return {'message': 'File successfully uploaded', 'filename': file.filename}, 200

# Create tabel pertama
@create_dataset.route("/create-dataset-table")
def create_dataset_table():
    db.create_all()
    df = pd.read_csv('./dataset/bencana-news.csv').drop_duplicates(subset=['full_text']).dropna(subset=['full_text'])
    df = df.where(pd.notnull(df), None)
    for index, row in df.iterrows():
        new_entry = Dataset(conversation_id_str=row['conversation_id_str'],
                              created_at=row['created_at'],
                              favorite_count=row['favorite_count'],
                              full_text=row['full_text'],
                              id_str=row['id_str'],
                              image_url=row['image_url'],
                              in_reply_to_screen_name=row['in_reply_to_screen_name'],
                              lang=row['lang'],
                              location=row['location'],
                              quote_count=row['quote_count'],
                              reply_count=row['reply_count'],
                              retweet_count=row['retweet_count'],
                              tweet_url=row['tweet_url'],
                              user_id_str=row['user_id_str'],
                              username=row['username'],
                              category=row['category'],
                              relevansi=row['relevansi'],
                              tipe_akun=row['tipe_akun'],
                              )
        db.session.add(new_entry)
    db.session.commit()
    return "Tabel dataset berhasil dibuat dan diisi dengan data."


# get data
@create_dataset.route('/get-dataset')
def get_dataset():
    data = call_dataset_obj()
    kategori_column = [row['category'] for row in data]
    relevansi_column = [row['relevansi'] for row in data]
    tipeakun_column = [row['tipe_akun'] for row in data]

    # Hitung frekuensi setiap kategori
    kategori_counter = Counter(kategori_column)
    relevansi_counter = Counter(relevansi_column)
    tipeakun_counter = Counter(tipeakun_column)

    # Ubah hasil ke format yang bisa dijadikan JSON
    kategori_json = [{"kategori": kategori, "jumlah": jumlah} for kategori, jumlah in kategori_counter.items()]
    relevansi_json = [{"relevansi": relevansi, "jumlah_relevansi": jumlah_relevansi} for relevansi, jumlah_relevansi in relevansi_counter.items()]
    tipeakun_json = [{"tipeakun": tipeakun, "jumlah_tipeakun": jumlah_tipeakun} for tipeakun, jumlah_tipeakun in tipeakun_counter.items()]

    # Membuat dictionary yang berisi data asli, kategori_json, relevansi_json, tipeakun_json, dan persentase perbedaan
    total = {
        "data": data,
        "category": kategori_json,
        "relevansi": relevansi_json,
        "tipeakun": tipeakun_json,
    }

    return jsonify(total)

@create_dataset.route("/get-csv")
def get_csv():
    data = call_dataset_obj()
    datacsv = pd.DataFrame(data)
    return datacsv.to_csv('./dataset/bencana-latest.csv', index=False)