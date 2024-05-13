import pandas as pd

lexicon_df = pd.read_csv('dataset/Indonesian-NRC-EmoLex.txt', delimiter='\t')
# Fungsi untuk mengkategorikan teks
def categorize_text(text):
    # Inisialisasi kategori
    categories = {
        'anger': 0,
        'anticipation': 0,
        'disgust': 0,
        'fear': 0,
        'joy': 0,
        'negative': 0,
        'positive': 0,
        'sadness': 0,
        'surprise': 0,
        'trust': 0
    }

    # Loop melalui setiap kata dalam teks
    for word in text.split():
        # Cari kata dalam lexicon
        match = lexicon_df[lexicon_df['Indonesian Word'] == word.lower()]
        if not match.empty:
            # Update kategori sesuai dengan lexicon
            for col in categories.keys():
                categories[col] += match[col].values[0]

    # Ambil kategori yang memiliki nilai maksimum
    max_category = max(categories, key=categories.get)

    return max_category