import re
import os
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
from collections import defaultdict

stop_words_paht = 'data/reuters/stopwords'
data_directory = 'data/reuters/training/'
filenames = os.listdir(data_directory)
filenames.sort(key=lambda x: int(x))
lemmatizer = WordNetLemmatizer()
word_counts = defaultdict(int)
wset = set()
nltk.download('stopwords')
stop_words2 = set(stopwords.words('english'))
stem_docs = {}
real_doc = {}
stop_words = []


def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


with open(stop_words_paht, 'r') as file:
    content = file.read().split('\n')
    stop_words.append(content)


def load_data():
    for filename in filenames:
        with open(os.path.join(data_directory, filename), 'r') as file:
            content = file.read()
            real_doc[filename] = content
            content = normalize_text(content)
            sdoc = []
            for word in content.lower().translate(str.maketrans('', '', string.punctuation)).split(" "):
                if word not in stop_words[0] or word not in stop_words2:
                    word = lemmatizer.lemmatize(word)
                    if word not in stop_words[0] or word not in stop_words2:
                        wset.add(word)
                        word_counts[word] += 1
                        sdoc.append(word)
            sdoc_concatenates = " ".join(sdoc)
            stem_docs[filename] = sdoc_concatenates


def load_data_to_dataframe():
    load_data()
    filenames_list = []
    original_text_list = []
    stemmed_text_list = []

    # Iterar sobre cada nombre de archivo y sus correspondientes textos originales y procesados
    for filename, original_text in real_doc.items():
        filenames_list.append(filename)
        original_text_list.append(original_text)
        stemmed_text_list.append(stem_docs[filename])

    # Crear el DataFrame
    df = pd.DataFrame({
        'filename': filenames_list,
        'original_text': original_text_list,
        'stemmed_text': stemmed_text_list
    })
    return df
