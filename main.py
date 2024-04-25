from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
cors = CORS(app, origins='*')

@app.route("/get-data")
def get_data():
    df = pd.read_csv('./dataset/eminatest.csv', nrows=10)
    # Ubah orientasi menjadi 'records' untuk mendapatkan objek JSON tanpa indeks
    return df.to_json(orient='records')

if __name__ == "__main__":
    app.run(debug=True)
