from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from models.model import db
from routes.testing_routes import testing
from routes.create_palestinatable import create_table_palestina
from routes.clean_regex import clean_text_regex
from routes.clean_preprocessing import clean_preprocessing
from routes.traindata_categorized import traindata
from routes.labeling_testdata import testdata_labeled

load_dotenv()
app = Flask(__name__)
cors = CORS(app, origins='*')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
db.init_app(app)


# testing routes
app.register_blueprint(testing)


# tabel pertama
app.register_blueprint(create_table_palestina)


# clean using regex
app.register_blueprint(clean_text_regex)


# clean text preprocessing
app.register_blueprint(clean_preprocessing)


# traindata preprocessing
app.register_blueprint(traindata)


# abeling
app.register_blueprint(testdata_labeled)



if __name__ == "__main__":
    app.run(debug=True)
