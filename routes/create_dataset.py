from flask import Blueprint, jsonify, request
import pandas as pd
from function.obj_converter import call_dataset_obj
from main import db
from models.model import Dataset
import os

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
    return jsonify(data)