import pandas as pd

# Lexicon bencana, dapat diperluas sesuai kebutuhan
disaster_lexicon = {
    'banjir': ['banjir', 'genangan', 'hujan deras', 'meluap'],
    'longsor': ['longsor', 'tanah longsor', 'erosi', 'lereng'],
    'gempa': ['gempa', 'seismik', 'tsunami', 'getaran'],
    'kebakaran': ['kebakaran', 'api', 'terbakar', 'kobaran'],
    'gunung meletus': ['meletus', 'lava', 'vulkanik', 'abu vulkanik'],
}

# Fungsi untuk mengkategorikan teks berdasarkan bencana
def categorize_text(text):
    # Inisialisasi kategori
    categories = {key: 0 for key in disaster_lexicon.keys()}

    # Loop melalui setiap kata dalam teks
    for word in text.split():
        for disaster, keywords in disaster_lexicon.items():
            if word.lower() in keywords:
                categories[disaster] += 1

    # Ambil semua kategori yang memiliki nilai di atas 0
    relevant_categories = [category for category, count in categories.items() if count > 0]

    return relevant_categories

# Contoh penggunaan
'''
text = "Terjadi banjir dan longsor di daerah tersebut setelah hujan deras semalaman."
categories = categorize_text(text)
print(f"Teks tersebut dikategorikan sebagai: {categories}")
'''
