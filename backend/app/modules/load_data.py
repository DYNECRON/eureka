import re
import os
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

stop_words_path = 'data/reuters/stopwords'
data_directory = 'data/reuters/training/'
filenames = os.listdir(data_directory)
filenames.sort(key=lambda x: int(x))
lemmatizer = WordNetLemmatizer()
nltk.download('stopwords')
stop_words_nltk = set(stopwords.words('english'))
processed_doc = {}
real_doc = {}
stop_words = []


def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


with open(stop_words_path, 'r') as file:
    content = file.read().split('\n')
    stop_words.append(content)


def load_data():
    for filename in filenames:
        with open(os.path.join(data_directory, filename), 'r') as file:
            content = file.read()
            real_doc[filename] = content
            content = normalize_text(content)
            words_list = []
            for word in content.translate(str.maketrans('', '', string.punctuation)).split(" "):
                if word not in stop_words[0] or word not in stop_words_nltk:
                    word = lemmatizer.lemmatize(word)
                    words_list.append(word)
            lemmatized_doc = " ".join(words_list)
            processed_doc[filename] = lemmatized_doc


def load_data_to_dataframe():
    load_data()
    filenames_list = []
    original_text_list = []
    processed_text = []

    # Iterar sobre cada nombre de archivo y sus correspondientes textos originales y procesados
    for filename, original_text in real_doc.items():
        filenames_list.append(filename)
        original_text_list.append(original_text)
        processed_text.append(processed_doc[filename])

    # Crear el DataFrame
    df = pd.DataFrame({
        'filename': filenames_list,
        'original_text': original_text_list,
        'processed_text': processed_text
    })
    return df
