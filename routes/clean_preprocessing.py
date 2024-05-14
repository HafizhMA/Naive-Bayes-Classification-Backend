from flask import Blueprint, jsonify
from function.obj_converter import call_palestinacleaned_obj, call_palestina_obj
from function.text_cleaner import clear_twitter_text
from function.normalisasi import normalize_text, norm
from function.stopwords import stopword
from function.stemming import stemming
from models.model import db, PalestinaCleaned

clean_preprocessing = Blueprint('clean_preprocessing', __name__, template_folder='routes')

@clean_preprocessing.route("/preprocessing-normalisasi")
def preprocessingNormalisasi():
    # Get data dari function.obj_converter.py
    data_list = call_palestina_obj()

    # Clean 'full_text' 
    for data in data_list:
        data['full_text'] = clear_twitter_text(data['full_text'])
        data['full_text'] = data['full_text'].lower()
        data['full_text'] = normalize_text(data['full_text'], norm)
    return jsonify(data_list)

@clean_preprocessing.route("/preprocessing-stopwords")
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

@clean_preprocessing.route("/preprocessing-tokenized")
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


@clean_preprocessing.route("/preprocessing-stemming-table")
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

@clean_preprocessing.route("/get-preprocessing-stemming")
def preprocessingStemming():
    data = call_palestinacleaned_obj()
    return jsonify(data)