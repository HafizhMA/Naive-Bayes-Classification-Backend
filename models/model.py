from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user' 
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.nama
    
class Dataset(db.Model):
    __tablename__ = 'dataset'
    id = db.Column(db.Integer, primary_key=True)
    conversation_id_str = db.Column(db.String(50))
    created_at = db.Column(db.String(100))
    favorite_count = db.Column(db.Integer)
    full_text = db.Column(db.String(500))
    id_str = db.Column(db.String(50))
    image_url = db.Column(db.String(200))
    in_reply_to_screen_name = db.Column(db.String(100))
    lang = db.Column(db.String(10))
    location = db.Column(db.String(100))
    quote_count = db.Column(db.Integer)
    reply_count = db.Column(db.Integer)
    retweet_count = db.Column(db.Integer)
    tweet_url = db.Column(db.String(200))
    user_id_str = db.Column(db.String(50))
    username = db.Column(db.String(100))
    category = db.Column(db.String(100))  
    relevansi = db.Column(db.String(100))  
    tipe_akun = db.Column(db.String(100))

    def __repr__(self):
        return '<Dataset %r>' % self.full_text
    
class Training(db.Model):
    __tablename__ = 'training'
    id = db.Column(db.Integer, primary_key=True)
    conversation_id_str = db.Column(db.String(50))
    created_at = db.Column(db.String(100))
    favorite_count = db.Column(db.Integer)
    full_text = db.Column(db.String(500))
    id_str = db.Column(db.String(50))
    image_url = db.Column(db.String(200))
    in_reply_to_screen_name = db.Column(db.String(100))
    lang = db.Column(db.String(10))
    location = db.Column(db.String(100))
    quote_count = db.Column(db.Integer)
    reply_count = db.Column(db.Integer)
    retweet_count = db.Column(db.Integer)
    tweet_url = db.Column(db.String(200))
    user_id_str = db.Column(db.String(50))
    username = db.Column(db.String(100))
    category = db.Column(db.String(100))  
    relevansi = db.Column(db.String(100))  
    tipe_akun = db.Column(db.String(100))

    def __repr__(self):
        return '<Training %r>' % self.full_text

class Testing(db.Model):
    __tablename__ = 'testing'
    id = db.Column(db.Integer, primary_key=True)
    conversation_id_str = db.Column(db.String(50))
    created_at = db.Column(db.String(100))
    favorite_count = db.Column(db.Integer)
    full_text = db.Column(db.String(500))
    id_str = db.Column(db.String(50))
    image_url = db.Column(db.String(200))
    in_reply_to_screen_name = db.Column(db.String(100))
    lang = db.Column(db.String(10))
    location = db.Column(db.String(100))
    quote_count = db.Column(db.Integer)
    reply_count = db.Column(db.Integer)
    retweet_count = db.Column(db.Integer)
    tweet_url = db.Column(db.String(200))
    user_id_str = db.Column(db.String(50))
    username = db.Column(db.String(100))
    category = db.Column(db.String(100))  
    relevansi = db.Column(db.String(100))  
    tipe_akun = db.Column(db.String(100))

    def __repr__(self):
        return '<Testing %r>' % self.full_text

class DatasetCleaned(db.Model):
    __tablename__ = 'datasetcleaned'
    id = db.Column(db.Integer, primary_key=True)
    conversation_id_str = db.Column(db.String(50))
    created_at = db.Column(db.String(100))
    favorite_count = db.Column(db.Integer)
    full_text = db.Column(db.String(500))
    id_str = db.Column(db.String(50))
    image_url = db.Column(db.String(200))
    in_reply_to_screen_name = db.Column(db.String(100))
    lang = db.Column(db.String(10))
    location = db.Column(db.String(100))
    quote_count = db.Column(db.Integer)
    reply_count = db.Column(db.Integer)
    retweet_count = db.Column(db.Integer)
    tweet_url = db.Column(db.String(200))
    user_id_str = db.Column(db.String(50))
    username = db.Column(db.String(100))
    category = db.Column(db.String(100))  
    relevansi = db.Column(db.String(100))  
    tipe_akun = db.Column(db.String(100))

    def __repr__(self):
        return '<DatasetCleaned %r>' % self.full_text
    
class LabeledDataTesting(db.Model):
    __tablename__ = 'labeleddatatesting'
    id = db.Column(db.Integer, primary_key=True)
    conversation_id_str = db.Column(db.String(50))
    created_at = db.Column(db.String(100))
    favorite_count = db.Column(db.Integer)
    full_text = db.Column(db.String(500))
    id_str = db.Column(db.String(50))
    image_url = db.Column(db.String(200))
    in_reply_to_screen_name = db.Column(db.String(100))
    lang = db.Column(db.String(10))
    location = db.Column(db.String(100))
    quote_count = db.Column(db.Integer)
    reply_count = db.Column(db.Integer)
    retweet_count = db.Column(db.Integer)
    tweet_url = db.Column(db.String(200))
    user_id_str = db.Column(db.String(50))
    username = db.Column(db.String(100))
    category = db.Column(db.String(100))
    relevansi = db.Column(db.String(255))
    tipe_akun = db.Column(db.String(255))
    category_naive_bayes = db.Column(db.String(255))

    def __repr__(self):
        return '<labeledDataTesting %r>' % self.full_text
