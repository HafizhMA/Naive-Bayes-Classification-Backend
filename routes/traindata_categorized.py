from flask import Blueprint, jsonify
from collections import Counter
from function.obj_converter import call_DatasetCleaned_obj, call_trainingdata_obj
from function.categorize_trainingdata import categorize_text
from models.model import db, DatasetTrainingData

traindata = Blueprint('traindata', __name__, template_folder='routes')

@traindata.route("/traindata-categorized")
def traindata_categorized():
    db.create_all()
    dataset_df = call_DatasetCleaned_obj()
    for data in dataset_df:
        categories = categorize_text(data['full_text'])
        
        # Hanya lanjutkan jika categories tidak kosong
        if categories:
            # Gabungkan daftar kategori menjadi string
            categories_str = ','.join(categories)
            new_entry = DatasetTrainingData(conversation_id_str=data['conversation_id_str'],
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
                                            categories=categories_str)  # Simpan sebagai string
            db.session.add(new_entry)
    db.session.commit()
    return "Table training data berhasil dibuat dan diisi dengan data."

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