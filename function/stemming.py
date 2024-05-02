from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
# Function to perform stemming
def stemming(text_cleaning):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    do = []
    for w in text_cleaning:
        dt = stemmer.stem(w)
        do.append(dt)
    d_clean = " ".join(do)
    return d_clean