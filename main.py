from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from models.model import db
from routes.testing_routes import testing
from routes.create_dataset import create_dataset
from routes.clean_regex import clean_text_regex
from routes.clean_preprocessing import clean_preprocessing
from routes.traindata_categorized import traindata
from routes.labeling_testdata import testdata_labeled
from routes.register_login import registerlogin
from flask_jwt_extended import JWTManager

load_dotenv()
app = Flask(__name__)
cors = CORS(app, origins='*')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv("SECRET_JWT")
db.init_app(app)
jwt = JWTManager(app)

# testing routes
app.register_blueprint(testing)


# tabel pertama
app.register_blueprint(create_dataset)


# clean using regex
app.register_blueprint(clean_text_regex)


# clean text preprocessing
app.register_blueprint(clean_preprocessing)


# traindata preprocessing
app.register_blueprint(traindata)


# labeling
app.register_blueprint(testdata_labeled)

# registerlogin
app.register_blueprint(registerlogin)



if __name__ == "__main__":
    app.run(debug=True)
