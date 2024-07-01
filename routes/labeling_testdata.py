from flask import Blueprint, jsonify
from collections import Counter
from function.obj_converter import call_DatasetCleaned_obj, call_trainingdata_obj, call_testingdata_obj, call_labeleddata_obj
import pandas as pd
from models.model import db, LabeledDataTesting, Testing, Training


testdata_labeled = Blueprint('testdata_labeled', __name__, template_folder='routes')

# labeling
@testdata_labeled.route("/labeling-testingdata")
def labeling_testdata():
    db.create_all()

    # Load data
    train_data = call_trainingdata_obj()
    test_data = call_testingdata_obj()

    # Convert train_data and test_data to DataFrames
    train_df = pd.DataFrame(train_data)
    test_df = pd.DataFrame(test_data)

    # Menghitung jumlah kategori dan kata-kata unik dalam data pelatihan
    categories = train_df['category'].unique()
    V = len(train_df['full_text'].str.split().explode().unique())  # Vocab size
    W = len(categories)  # Jumlah kategori

    # Menghitung probabilitas prior untuk setiap kategori P(Vj)
    prior_probs = {}
    for category in categories:
        prior_probs[category] = len(train_df[train_df['category'] == category]) / len(train_df)

    # Membuat fungsi untuk menghitung probabilitas kondisional P(xi|Vj)
    def conditional_prob(word, category, train_data):
        word_count_in_category = train_data[train_data['category'] == category]['full_text'].str.split().apply(lambda x: x.count(word)).sum()
        total_words_in_category = train_data[train_data['category'] == category]['full_text'].str.split().apply(len).sum()
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
    test_df['category_naive_bayes'] = predictions

    # Save labeled data into the database
    for i, data in enumerate(test_data):
        new_entry = LabeledDataTesting(
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
            category=data['category'],
            relevansi=data['relevansi'],
            tipe_akun=data['tipe_akun'],
            category_naive_bayes=predictions[i]
        )
        db.session.add(new_entry)

    db.session.commit()
    return "The labeled data testing table has been successfully created and populated."

# get data
@testdata_labeled.route('/get-training-data')
def get_training_dataset():
    data = call_trainingdata_obj()
    return jsonify(data)

@testdata_labeled.route('/get-testing-data')
def get_testing_data():
    data = call_testingdata_obj()
    return jsonify(data)

@testdata_labeled.route("/get-relevance-datatraining")
def get_relevance_datatraining():
    data = call_trainingdata_obj()

    # Ambil kolom yang berisi kategori
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

@testdata_labeled.route("/get-relevance-datatesting")
def get_relevance_datatesting():
    data = call_testingdata_obj()

    # Ambil kolom yang berisi kategori
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

@testdata_labeled.route("/get-relevance-labeleddata")
def get_relevance_labeleddata():
    data = call_labeleddata_obj()

    # Ambil kolom yang berisi kategori
    kategori_column = [row['category'] for row in data]
    relevansi_column = [row['relevansi'] for row in data]
    tipeakun_column = [row['tipe_akun'] for row in data]
    naivebayes_category = [row['category_naive_bayes'] for row in data]

    # Hitung frekuensi setiap kategori
    kategori_counter = Counter(kategori_column)
    relevansi_counter = Counter(relevansi_column)
    tipeakun_counter = Counter(tipeakun_column)
    naivebayes_category_counter = Counter(naivebayes_category)

    # Ubah hasil ke format yang bisa dijadikan JSON
    kategori_json = [{"kategori": kategori, "jumlah": jumlah} for kategori, jumlah in kategori_counter.items()]
    relevansi_json = [{"relevansi": relevansi, "jumlah_relevansi": jumlah_relevansi} for relevansi, jumlah_relevansi in relevansi_counter.items()]
    tipeakun_json = [{"tipeakun": tipeakun, "jumlah_tipeakun": jumlah_tipeakun} for tipeakun, jumlah_tipeakun in tipeakun_counter.items()]
    naive_bayes_json = [{"kategori": kategori, "jumlah": jumlah} for kategori, jumlah in naivebayes_category_counter.items()]

    # Membuat dictionary yang berisi data asli, kategori_json, relevansi_json, tipeakun_json, dan persentase perbedaan
    total = {
        "data": data,
        "category": kategori_json,
        "relevansi": relevansi_json,
        "tipeakun": tipeakun_json,
        "category_naive_bayes": naive_bayes_json,
    }

    return jsonify(total)

@testdata_labeled.route('/split-data')
def split_data():
    # Load your dataset, split it into train_df and test_df here
    sql_df = call_DatasetCleaned_obj()
    df = pd.DataFrame(sql_df)
    total_rows = len(df)
    train_rows = int(0.8 * total_rows)
    test_rows = total_rows - train_rows

    train_df = df.iloc[:train_rows]
    test_df = df.iloc[train_rows:train_rows + test_rows]

    # Create tables if they do not exist
    db.create_all()

    # Save train_df and test_df to SQL
    save_to_sql(train_df, Training)
    save_to_sql(test_df, Testing)

    return "Data berhasil dibagi dan disimpan ke SQL."

def save_to_sql(df, model):
    for index, row in df.iterrows():
        new_entry = model(
            conversation_id_str=row['conversation_id_str'],
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
            tipe_akun=row['tipe_akun']
        )
        db.session.add(new_entry)
    db.session.commit()