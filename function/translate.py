import pandas as pd
from googletrans import Translator

# Translate the Text
def convert_eng(tweet):
    translator = Translator()
    translation = translator.translate(tweet, src='id', dest='en')
    return translation.text