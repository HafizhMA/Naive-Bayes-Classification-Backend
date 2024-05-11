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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/analisisemosi'
db = SQLAlchemy(app)
cors = CORS(app, origins='*')


# init Model
class User(db.Model):
    __tablename__ = 'user' 
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.nama
    
class Palestina(db.Model):
    __tablename__ = 'palestina'
    id = db.Column(db.Integer, primary_key=True)
    conversation_id_str = db.Column(db.String(50))
    created_at = db.Column(db.String(100))
    favorite_count = db.Column(db.Integer)
    full_text = db.Column(db.String(500))
    id_str = db.Column(db.String(50))
    image_url = db.Column(db.String(200))
    in_reply_to_screen_name = db.Column(db.String(100))
    lang = db.Column(db.String(10))
    location = db.Column(db.String(100))
    quote_count = db.Column(db.Integer)
    reply_count = db.Column(db.Integer)
    retweet_count = db.Column(db.Integer)
    tweet_url = db.Column(db.String(200))
    user_id_str = db.Column(db.String(50))
    username = db.Column(db.String(100))

    def __repr__(self):
        return '<Palestina %r>' % self.full_text


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


# get all data from table
@app.route("/get-all-palestina-data")
def get_all_palestina_data():
    all_data = Palestina.query.all()
    data_list = []
    for data in all_data:
        data_dict = {
            'id': data.id,
            'conversation_id_str': data.conversation_id_str,
            'created_at': data.created_at,
            'favorite_count': data.favorite_count,
            'full_text': data.full_text,
            'id_str': data.id_str,
            'image_url': data.image_url,
            'in_reply_to_screen_name': data.in_reply_to_screen_name,
            'lang': data.lang,
            'location': data.location,
            'quote_count': data.quote_count,
            'reply_count': data.reply_count,
            'retweet_count': data.retweet_count,
            'tweet_url': data.tweet_url,
            'user_id_str': data.user_id_str,
            'username': data.username
        }
        data_list.append(data_dict)
    return jsonify(data_list)

@app.route('/')
def index():
    users = User.query.all()
    user_data = [{'id': user.id, 'nama': user.nama} for user in users]
    return jsonify(user_data)


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
