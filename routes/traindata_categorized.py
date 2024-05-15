from flask import Blueprint, jsonify
from collections import Counter
from function.obj_converter import call_palestinacleaned_obj, call_trainingdata_obj
from function.categorize_trainingdata import categorize_text
from models.model import db, PalestinaTrainingData

traindata = Blueprint('traindata', __name__, template_folder='routes')

@traindata.route("/traindata-categorized")
def traindata_categorized():
    db.create_all()
    palestine_df = call_palestinacleaned_obj()
    for data in palestine_df:
        categories = categorize_text(data['full_text'])
        new_entry = PalestinaTrainingData(conversation_id_str=data['conversation_id_str'],
                                          created_at=data['created_at'],
                                          favorite_count=data['favorite_count'],
                                          full_text=data['full_text'],
                                          id_str=data['id_str'],
                                          image_url=data['image_url'],
                                          in_reply_to_screen_name=data['in_reply_to_screen_name'],
                                          lang=data['lang'],
                                          location=data['location'],
                                          quote_count=data['quote_count'],
                                          reply_count=data['reply_count'],
                                          retweet_count=data['retweet_count'],
                                          tweet_url=data['tweet_url'],
                                          user_id_str=data['user_id_str'],
                                          username=data['username'],
                                          categories=categories)
        db.session.add(new_entry)
    db.session.commit()
    return "Table training data Palestina berhasil dibuat dan diisi dengan data."

@traindata.route("/get-trainingdata")
def get_training_data():
    data = call_trainingdata_obj()
    return jsonify(data)

@traindata.route("/get-kategori-trainingdata")
def get_kategori():
    data = call_trainingdata_obj()
    
    # Ambil kolom yang berisi kategori
    kategori_column = [row['categories'] for row in data]
    
    # Hitung frekuensi setiap kategori
    kategori_counter = Counter(kategori_column)
    
    # Ubah hasil ke format yang bisa dijadikan JSON
    kategori_json = [{"kategori": kategori, "jumlah": jumlah} for kategori, jumlah in kategori_counter.items()]
    # Membuat dictionary yang berisi data asli dan kategori_json
    total = {"datas": data, "categories": kategori_json}
    
    return jsonify(total)