from flask import Flask
from flask_cors import CORS
import pandas as pd
from function.text_cleaner import clear_twitter_text
from function.normalisasi import normalize_text, norm

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
def preprocessing():
    df = pd.read_csv('./dataset/eminatest.csv')
    df = df.drop_duplicates(subset=["full_text"])
    df= df.dropna(subset=["full_text"])
    df['full_text'] = df['full_text'].apply(clear_twitter_text)
    df['full_text'] = df['full_text'].str.lower()
    df['full_text'] = df['full_text'].apply(lambda x: normalize_text(x, norm))
    return df.to_json(orient='records')


if __name__ == "__main__":
    app.run(debug=True)
