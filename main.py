from flask import Flask, jsonify
from collections import Counter
from flask_cors import CORS
import pandas as pd
from textblob import TextBlob
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import preprocessor as p
from function.text_cleaner import clear_twitter_text
from function.normalisasi import normalize_text, norm
from function.stopwords import stopword
from function.stemming import stemming
from function.translate import convert_eng
from function.categorize_trainingdata import categorize_text
from function.obj_converter import call_palestina_obj, call_palestinacleaned_obj, call_trainingdata_obj
from models.model import db, User, Palestina, PalestinaCleaned, PalestinaTrainingData

app = Flask(__name__)
cors = CORS(app, origins='*')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/analisisemosi'
db.init_app(app)


# test connect flask
@app.route("/")
def home():
    return 'connect ke flask berhasil'


# Create and insert table
@app.route("/create-palestina-table")
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


# get semua data
@app.route('/get-palestina-data')
def get_palestina_data():
    data = call_palestina_obj()
    return jsonify(data)

@app.route("/get-preprocessing-stemming")
def preprocessingStemming():
    data = call_palestinacleaned_obj()
    return jsonify(data)

@app.route("/get-trainingdata")
def get_training_data():
    data = call_trainingdata_obj()
    return jsonify(data)

@app.route("/get-kategori-trainingdata")
def get_kategori():
    data = call_trainingdata_obj()
    
    # Ambil kolom yang berisi kategori
    kategori_column = [row['categories'] for row in data]
    
    # Hitung frekuensi setiap kategori
    kategori_counter = Counter(kategori_column)
    
    # Ubah hasil ke format yang bisa dijadikan JSON
    kategori_json = [{"kategori": kategori, "jumlah": jumlah} for kategori, jumlah in kategori_counter.items()]
    # Membuat dictionary yang berisi data asli dan kategori_json
    total = {"data": data, "kategori": kategori_json}
    
    return jsonify(total)




# cleaning data
@app.route("/clean-text")
def clean_text():
    # Get data dari function.obj_converter.py
    data_list = call_palestina_obj()

    # Clean 'full_text' 
    for data in data_list:
        data['full_text'] = clear_twitter_text(data['full_text'])

    return jsonify(data_list)


# preprocessing
@app.route("/preprocessing-normalisasi")
def preprocessingNormalisasi():
    # Get data dari function.obj_converter.py
    data_list = call_palestina_obj()

    # Clean 'full_text' 
    for data in data_list:
        data['full_text'] = clear_twitter_text(data['full_text'])
        data['full_text'] = data['full_text'].lower()
        data['full_text'] = normalize_text(data['full_text'], norm)
    return jsonify(data_list)

@app.route("/preprocessing-stopwords")
def preprocessingStopwords():
    # Get data dari function.obj_converter.py
    data_list = call_palestina_obj()

    # Clean 'full_text' 
    for data in data_list:
        data['full_text'] = clear_twitter_text(data['full_text'])
        data['full_text'] = data['full_text'].lower()
        data['full_text'] = normalize_text(data['full_text'], norm)
        data['full_text'] = stopword(data['full_text'])
    return jsonify(data_list)

@app.route("/preprocessing-tokenized")
def preprocessingTokenized():
    # Get data dari function.obj_converter.py
    data_list = call_palestina_obj()

    # Clean 'full_text' 
    for data in data_list:
        data['full_text'] = clear_twitter_text(data['full_text'])
        data['full_text'] = data['full_text'].lower()
        data['full_text'] = normalize_text(data['full_text'], norm)
        data['full_text'] = stopword(data['full_text'])
        data['full_text'] = data['full_text'].split()
    return jsonify(data_list)


@app.route("/preprocessing-stemming-table")
def preprocessingStemmingTable():
    db.create_all()
    # Assuming call_palestina_obj() fetches data as a list of dictionaries
    data_list = call_palestina_obj()

    # Clean 'full_text' 
    for data in data_list:
        data['full_text'] = clear_twitter_text(data['full_text'])
        data['full_text'] = data['full_text'].lower()
        data['full_text'] = normalize_text(data['full_text'], norm)
        data['full_text'] = stopword(data['full_text'])
        data['full_text'] = data['full_text'].split()
        data['full_text'] = stemming(data['full_text'])

        new_entry = PalestinaCleaned(conversation_id_str=data['conversation_id_str'],
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
                              username=data['username'])
        db.session.add(new_entry)
    db.session.commit()
    return "Tabel Palestinacleaned berhasil dibuat dan diisi dengan data."

@app.route("/traindata-categorized")
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

# labeling
@app.route("/labeling-textblob")
def labelingTextblob():
    # jangan lupa download nltk, uncomment code dibawah
    # nltk.download('punkt')
    df = pd.read_csv('./dataset/eminacleantranslate.csv')
    df = df.drop_duplicates(subset=["full_text"])
    df = df.dropna(subset=["full_text"])
    data_tweet = list(df['tweet_english'])

    polaritas = 0
    status = []
    total_suka = total_tidaksuka = total_netral = total = 0

    for i, tweet in enumerate(data_tweet):
        analysis = TextBlob(tweet)
        polaritas += analysis.polarity

        if analysis.sentiment.polarity > 0.0:
            total_suka += 1
            status.append('Suka')
        elif analysis.sentiment.polarity == 0.0:
            total_netral += 1
            status.append('Netral')
        else:
            total_tidaksuka += 1
            status.append('Tidak_suka')

        total += 1

    result = [{
        'suka': total_suka,
        'netral': total_netral,
        'tidaksuka': total_tidaksuka,
        'totaldata': total
    }]

    df['klasifikasi_textblob'] = status

    df_json = df.to_json(orient='records')

    # Menggabungkan DataFrame JSON dan result ke dalam satu dictionary
    response_data = {
        'df': df_json,
        'result': result
    }

    return (response_data)



if __name__ == "__main__":
    app.run(debug=True)
