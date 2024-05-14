from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user' 
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.nama
    
class Palestina(db.Model):
    __tablename__ = 'palestina'
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

    def __repr__(self):
        return '<Palestina %r>' % self.full_text

class PalestinaCleaned(db.Model):
    __tablename__ = 'palestinacleaned'
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

    def __repr__(self):
        return '<Palestinacleaned %r>' % self.full_text
    
class PalestinaTrainingData(db.Model):
    __tablename__ = 'palestinatrainingdata'
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
    categories = db.Column(db.String(100))

    def __repr__(self):
        return '<PalestinaTrainingData %r>' % self.full_text
    
class LabeledPalestinaData(db.Model):
    __tablename__ = 'labeledpalestinadata'
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

    def __repr__(self):
        return '<labeledpalestinadata %r>' % self.full_text
