from flask import Blueprint, jsonify, request
from collections import Counter
from function.obj_converter import call_DatasetCleaned_obj, call_trainingdata_obj, call_testingdata_obj, call_labeleddata_obj
import pandas as pd
from models.model import db, LabeledDataTesting, Testing, Training
import random


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
    # Load your dataset
    sql_df = call_DatasetCleaned_obj()
    df = pd.DataFrame(sql_df)
    
    # Shuffle the dataframe randomly
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    # Calculate the number of rows for training and testing
    total_rows = len(df)
    train_rows = int(0.8 * total_rows)
    test_rows = total_rows - train_rows

    # Split data into train_df and test_df
    train_df = df.iloc[:train_rows]
    test_df = df.iloc[train_rows:total_rows]

    # Create tables if they do not exist (if using SQLAlchemy)
    db.create_all()

    # Save train_df and test_df to SQL
    save_to_sql(train_df, Training)
    save_to_sql(test_df, Testing)

    return "Data berhasil dibagi dan disimpan ke SQL."

def save_to_sql(df, model):
    for index, row in df.iterrows():
        # Adjust the following mapping based on your actual column names in df
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

@testdata_labeled.route('/update-labeled-data', methods=['POST'])
def update_labeled_data():
    data = request.get_json()
    tweet_id = data.get('id')
    new_category = data.get('category')

    tweet = LabeledDataTesting.query.get(tweet_id)
    if tweet:
        tweet.category = new_category
        db.session.commit()
        return jsonify({'message': 'Data updated successfully'}), 200
    else:
        return jsonify({'message': 'Tweet not found'}), 404

@testdata_labeled.route('/hitung_metrics', methods=['GET'])
def hitung_metrics():
    # Query untuk mendapatkan data prediksi
    predictions = call_labeleddata_obj()

    # Inisialisasi confusion matrix
    confusion_matrix = {
        'netral': {'netral': 0, 'banjir lahar dingin': 0, 'banjir': 0},
        'banjir lahar dingin': {'netral': 0, 'banjir lahar dingin': 0, 'banjir': 0},
        'banjir': {'netral': 0, 'banjir lahar dingin': 0, 'banjir': 0}
    }

    # Mengisi confusion matrix
    for pred in predictions:
        true_category = pred.category
        predicted_category = pred.category_naive_bayes
        confusion_matrix[true_category][predicted_category] += 1

    # Menghitung metrik untuk setiap kategori
    metrics = {}
    for category in confusion_matrix.keys():
        TP = confusion_matrix[category][category]
        FP = sum(confusion_matrix[other_category][category] for other_category in confusion_matrix if other_category != category)
        FN = sum(confusion_matrix[category][other_category] for other_category in confusion_matrix[category] if other_category != category)
        TN = sum(confusion_matrix[other_category][other_category_2] 
                 for other_category in confusion_matrix 
                 for other_category_2 in confusion_matrix[other_category] 
                 if other_category != category and other_category_2 != category)

        accuracy = (TP + TN) / (TP + FP + FN + TN) if (TP + FP + FN + TN) > 0 else 0
        precision = TP / (TP + FP) if (TP + FP) > 0 else 0
        recall = TP / (TP + FN) if (TP + FN) > 0 else 0
        f1_score = (2 * recall * precision) / (recall + precision) if (recall + precision) > 0 else 0

        # Mengubah metrik menjadi persentase
        accuracy *= 100
        precision *= 100
        recall *= 100
        f1_score *= 100

        metrics[category] = [{
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'TP': TP,
            'FP': FP,
            'FN': FN,
            'TN': TN
        }]

    return jsonify(metrics)




@testdata_labeled.route('/hitung_accuracy', methods=['GET'])
def hitung_accuracy():
    # Query untuk mendapatkan data prediksi
    predictions = LabeledDataTesting.query.all()

    # Inisialisasi variabel untuk metrik
    TP = 0  # True Positives
    FP = 0  # False Positives

    # Mengisi variabel metrik
    for pred in predictions:
        true_category = pred.category
        predicted_category = pred.category_naive_bayes
        if true_category == predicted_category:
            TP += 1
        else:
            FP += 1

    # Menghitung akurasi
    total_data = len(predictions)
    accuracy = TP / total_data if total_data > 0 else 0

    # Format output sebagai JSON
    result = [{
        'accuracy': accuracy * 100,
    }]

    return jsonify(result)