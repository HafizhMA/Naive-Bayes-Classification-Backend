from flask import Blueprint, jsonify
from function.obj_converter import call_dataset_obj
from function.text_cleaner import clear_twitter_text

clean_text_regex = Blueprint('clean_text_regex', __name__, template_folder='routes')

# cleaning data
@clean_text_regex.route("/clean-text")
def clean_text():
    # Get data dari function.obj_converter.py
    data_list = call_dataset_obj()

    # Clean 'full_text' 
    for data in data_list:
        data['full_text'] = clear_twitter_text(data['full_text'])

    return jsonify(data_list)