from flask import Flask
from flask_cors import CORS
import pandas as pd
from function.text_cleaner import clear_twitter_text
from function.normalisasi import normalize_text, norm
from function.stopwords import stopword
from function.stemming import stemming
from function.translate import convert_eng

app = Flask(__name__)
cors = CORS(app, origins='*')
#request
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

@app.route("/preprocessing-stemming")
def preprocessingStemming():
    df = pd.read_csv('./dataset/eminatest.csv')
    df = df.head(50)
    df = df.drop_duplicates(subset=["full_text"])
    df= df.dropna(subset=["full_text"])
    df['full_text'] = df['full_text'].apply(clear_twitter_text)
    df['full_text'] = df['full_text'].str.lower()
    df['full_text'] = df['full_text'].apply(lambda x: normalize_text(x, norm))
    df['full_text'] = df['full_text'].apply(stopword)
    df['full_text'] = df['full_text'].apply(lambda x:x.split())
    df['full_text'] = df['full_text'].apply(stemming)
    return df.to_json(orient='records')

@app.route("/preprocessing-stemmingcsv")
def preprocessingStemmingCsv():
    df = pd.read_csv('./dataset/eminatest.csv')
    df = df.drop_duplicates(subset=["full_text"])
    df= df.dropna(subset=["full_text"])
    df['full_text'] = df['full_text'].apply(clear_twitter_text)
    df['full_text'] = df['full_text'].str.lower()
    df['full_text'] = df['full_text'].apply(lambda x: normalize_text(x, norm))
    df['full_text'] = df['full_text'].apply(stopword)
    df['full_text'] = df['full_text'].apply(lambda x:x.split())
    df['full_text'] = df['full_text'].apply(stemming)
    return df.to_csv('./dataset/eminacleaned.csv', index=False)

@app.route("/preprocessing-translate")
def preprocessingTranslate():
    df = pd.read_csv('./dataset/eminacleantranslate.csv')
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


if __name__ == "__main__":
    app.run(debug=True)
