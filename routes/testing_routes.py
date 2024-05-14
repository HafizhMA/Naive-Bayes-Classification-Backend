from flask import Blueprint
import pandas as pd
from function.obj_converter import call_trainingdata_obj

testing = Blueprint('testing', __name__, template_folder='routes')

# testing route
@testing.route("/")
def home():
    return 'connect ke flask berhasil'

@testing.route("/sql-to-df")
def sqltodf():
    data = call_trainingdata_obj()
    df = pd.DataFrame(data)
    json_data = df.to_json(orient='records')
    # Return JSON response
    return json_data