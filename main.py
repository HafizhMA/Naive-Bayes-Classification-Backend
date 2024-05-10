from flask import Flask, jsonify
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
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'analisisemosi'
mysql = MySQL(app)
cors = CORS(app, origins='*')



#request
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user")
    data = cur.fetchall()
    cur.close()
    return str(data)
#showing data
@app.route("/get-data")
def get_data():
    df = pd.read_csv('./dataset/eminatest.csv')
    return df.to_json(orient='records')

#cleaning data
@app.route("/clean-text")
def clean_text():
    df = pd.read_csv('./dataset/eminatest.csv')
    df = df.drop_duplicates(subset=["full_text"])
    df= df.dropna(subset=["full_text"])
    df['full_text'] = df['full_text'].apply(clear_twitter_text)
    df['full_text'] = df['full_text'].str.lower()
    return df.to_json(orient='records')

#preprocessing
@app.route("/preprocessing-normalisasi")
def preprocessingNormalisasi():
    df = pd.read_csv('./dataset/eminatest.csv')
    df = df.drop_duplicates(subset=["full_text"])
    df= df.dropna(subset=["full_text"])
    df['full_text'] = df['full_text'].apply(clear_twitter_text)
    df['full_text'] = df['full_text'].str.lower()
    df['full_text'] = df['full_text'].apply(lambda x: normalize_text(x, norm))
    return df.to_json(orient='records')

@app.route("/preprocessing-stopwords")
def preprocessingStopwords():
    df = pd.read_csv('./dataset/eminatest.csv')
    df = df.drop_duplicates(subset=["full_text"])
    df= df.dropna(subset=["full_text"])
    df['full_text'] = df['full_text'].apply(clear_twitter_text)
    df['full_text'] = df['full_text'].str.lower()
    df['full_text'] = df['full_text'].apply(lambda x: normalize_text(x, norm))
    df['full_text'] = df['full_text'].apply(stopword)
    
    return df.to_json(orient='records')

@app.route("/preprocessing-tokenized")
def preprocessingTokenized():
    df = pd.read_csv('./dataset/eminatest.csv')
    df = df.drop_duplicates(subset=["full_text"])
    df= df.dropna(subset=["full_text"])
    df['full_text'] = df['full_text'].apply(clear_twitter_text)
    df['full_text'] = df['full_text'].str.lower()
    df['full_text'] = df['full_text'].apply(lambda x: normalize_text(x, norm))
    df['full_text'] = df['full_text'].apply(stopword)
    df['full_text'] = df['full_text'].apply(lambda x:x.split())
    return df.to_json(orient='records')


@app.route("/preprocessing-stemmingcsv")
def preprocessingStemmingCsv():
    df = pd.read_csv('./dataset/palestina.csv')
    df = df.drop_duplicates(subset=["full_text"])
    df= df.dropna(subset=["full_text"])
    df['full_text'] = df['full_text'].apply(clear_twitter_text)
    df['full_text'] = df['full_text'].str.lower()
    df['full_text'] = df['full_text'].apply(lambda x: normalize_text(x, norm))
    df['full_text'] = df['full_text'].apply(stopword)
    df['full_text'] = df['full_text'].apply(lambda x:x.split())
    df['full_text'] = df['full_text'].apply(stemming)
    return df.to_csv('./dataset/palestinacleaned.csv', index=False)

@app.route("/preprocessing-stemming")
def preprocessingStemming():
    df = pd.read_csv('./dataset/eminacleaned.csv')
    df = df.drop_duplicates(subset=["full_text"])
    df= df.dropna(subset=["full_text"])
    return df.to_json(orient='records')

@app.route("/preprocessing-translatecsv")
def preprocessingTranslateCsv():
    df = pd.read_csv('./dataset/eminacleaned.csv')
    df = df.drop_duplicates(subset=["full_text"])
    df= df.dropna(subset=["full_text"])
    df['tweet_english'] = df['full_text'].apply(convert_eng)
    return df.to_csv('./dataset/eminacleantranslate.csv', index=False)

@app.route("/preprocessing-translate")
def preprocessingTranslate():
    df = pd.read_csv('./dataset/eminacleantranslate.csv')
    df = df.drop_duplicates(subset=["full_text"])
    df= df.dropna(subset=["full_text"])
    return df.to_json(orient='records')

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
