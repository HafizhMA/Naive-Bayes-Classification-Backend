from sqlalchemy import create_engine, text
import os

# Get database URI from environment variable
engine = create_engine(os.getenv("DATABASE_URI"))

def call_dataset_obj():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM Dataset"))
        data_list = []
        for row in result:
            data_dict = {
                'id': row[0],
                'conversation_id_str': row[1],
                'created_at': row[2],
                'favorite_count': row[3],
                'full_text': row[4],
                'id_str': row[5],
                'image_url': row[6],
                'in_reply_to_screen_name': row[7],
                'lang': row[8],
                'location': row[9],
                'quote_count': row[10],
                'reply_count': row[11],
                'retweet_count': row[12],
                'tweet_url': row[13],
                'user_id_str': row[14],
                'username': row[15],
                'category': row[16],
                'relevansi': row[17],
                'tipe_akun': row[18]
            }
            data_list.append(data_dict)
    return data_list

def call_DatasetCleaned_obj():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM DatasetCleaned"))
        data_list = []
        for row in result:
            data_dict = {
                'id': row[0],
                'conversation_id_str': row[1],
                'created_at': row[2],
                'favorite_count': row[3],
                'full_text': row[4],
                'id_str': row[5],
                'image_url': row[6],
                'in_reply_to_screen_name': row[7],
                'lang': row[8],
                'location': row[9],
                'quote_count': row[10],
                'reply_count': row[11],
                'retweet_count': row[12],
                'tweet_url': row[13],
                'user_id_str': row[14],
                'username': row[15],
                'category': row[16],
                'relevansi': row[17],
                'tipe_akun': row[18]
            }
            data_list.append(data_dict)
    return data_list

def call_trainingdata_obj():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM DatasetTrainingData"))
        data_list = []
        for row in result:
            data_dict = {
                'id': row[0],
                'conversation_id_str': row[1],
                'created_at': row[2],
                'favorite_count': row[3],
                'full_text': row[4],
                'id_str': row[5],
                'image_url': row[6],
                'in_reply_to_screen_name': row[7],
                'lang': row[8],
                'location': row[9],
                'quote_count': row[10],
                'reply_count': row[11],
                'retweet_count': row[12],
                'tweet_url': row[13],
                'user_id_str': row[14],
                'username': row[15],
                'categories': row[16]
            }
            data_list.append(data_dict)
    return data_list

def call_labeleddata_obj():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM LabeledDataTesting"))
        data_list = []
        for row in result:
            data_dict = {
                'id': row[0],
                'conversation_id_str': row[1],
                'created_at': row[2],
                'favorite_count': row[3],
                'full_text': row[4],
                'id_str': row[5],
                'image_url': row[6],
                'in_reply_to_screen_name': row[7],
                'lang': row[8],
                'location': row[9],
                'quote_count': row[10],
                'reply_count': row[11],
                'retweet_count': row[12],
                'tweet_url': row[13],
                'user_id_str': row[14],
                'username': row[15],
                'category': row[16]
            }
            data_list.append(data_dict)
    return data_list
