from models.model import Palestina

# get semua data di tabel  model dan mereturn array berisi object
def call_palestina_obj():
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
    return data_list