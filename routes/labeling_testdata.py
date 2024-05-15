from flask import Blueprint, jsonify
from collections import Counter
from function.obj_converter import call_palestinacleaned_obj, call_trainingdata_obj, call_labeleddata_obj
import pandas as pd
from models.model import db, LabeledPalestinaData


testdata_labeled = Blueprint('testdata_labeled', __name__, template_folder='routes')

# labeling
@testdata_labeled.route("/labeling-testingdata")
def labeling_testdata():
    db.create_all()

    # Load data
    train_data = call_trainingdata_obj()
    test_data = call_palestinacleaned_obj()

    # Convert train_data and test_data to DataFrames
    train_df = pd.DataFrame(train_data)
    test_df = pd.DataFrame(test_data)

    # Menghitung jumlah kategori dan kata-kata unik dalam data pelatihan
    categories = train_df['categories'].unique()
    V = len(train_df['full_text'].str.split().explode().unique())  # Vocab size
    W = len(categories)  # Jumlah kategori

    # Menghitung probabilitas prior untuk setiap kategori P(Vj)
    prior_probs = {}
    for category in categories:
        prior_probs[category] = len(train_df[train_df['categories'] == category]) / len(train_df)

    # Membuat fungsi untuk menghitung probabilitas kondisional P(xi|Vj)
    def conditional_prob(word, category, train_data):
        word_count_in_category = train_data[train_data['categories'] == category]['full_text'].str.split().apply(lambda x: x.count(word)).sum()
        total_words_in_category = train_data[train_data['categories'] == category]['full_text'].str.split().apply(len).sum()
        return (word_count_in_category + 1) / (total_words_in_category + V)

    # Prediksi kategori untuk setiap dokumen di data pengujian
    predictions = []
    for index, row in test_df.iterrows():
        max_prob = -1
        pred_category = None
        for category in categories:
            prob = prior_probs[category]
            for word in row['full_text'].split():
                prob *= conditional_prob(word, category, train_df)
            if prob > max_prob:
                max_prob = prob
                pred_category = category
        predictions.append(pred_category)

    # Menambahkan kolom prediksi ke data pengujian
    test_df['predicted_category'] = predictions

    # Save labeled data into the database
    for i, data in enumerate(test_data):
        new_entry = LabeledPalestinaData(
            conversation_id_str=data['conversation_id_str'],
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
            category=predictions[i]
        )
        db.session.add(new_entry)

    db.session.commit()
    return "The labeled Palestine data table has been successfully created and populated."

@testdata_labeled.route("/get-labeled-testdata")
def get_labeled_testdata():
    data = call_labeleddata_obj()
    # Ambil kolom yang berisi kategori
    kategori_column = [row['category'] for row in data]
    
    # Hitung frekuensi setiap kategori
    kategori_counter = Counter(kategori_column)
    
    # Ubah hasil ke format yang bisa dijadikan JSON
    kategori_json = [{"kategori": kategori, "jumlah": jumlah} for kategori, jumlah in kategori_counter.items()]
    # Membuat dictionary yang berisi data asli dan kategori_json
    total = {"datas": data, "category": kategori_json}
    
    return jsonify(total)