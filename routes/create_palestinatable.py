from flask import Blueprint, jsonify
import pandas as pd
from function.obj_converter import call_palestina_obj
from main import db
from models.model import Palestina

create_table_palestina = Blueprint('create_table_palestina', __name__, template_folder='routes')

# Create tabel pertama
@create_table_palestina.route("/create-palestina-table")
def create_palestina_table():
    db.create_all()
    df = pd.read_csv('./dataset/palestina.csv').drop_duplicates(subset=['full_text']).dropna(subset=['full_text'])
    df = df.where(pd.notnull(df), None)
    for index, row in df.iterrows():
        new_entry = Palestina(conversation_id_str=row['conversation_id_str'],
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
                              username=row['username'])
        db.session.add(new_entry)
    db.session.commit()
    return "Tabel Palestina berhasil dibuat dan diisi dengan data."


# get data
@create_table_palestina.route('/get-palestina-data')
def get_palestina_data():
    data = call_palestina_obj()
    return jsonify(data)