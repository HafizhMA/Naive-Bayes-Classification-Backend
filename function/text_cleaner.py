import re

#regex untuk membersihkan data dari mention hashtag url dan spesial karakter
def clear_twitter_text(text):
    # Remove @mentions
    text = re.sub(r'@[A-Za-z0-9_]+', '', text)

    # Remove #hashtags
    text = re.sub(r'#[A-Za-z0-9_]+', '', text)

    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'www\S+', '', text)

    # Remove special characters
    text = re.sub(r'[^A-Za-z0-9 ]', ' ', text)

    return text