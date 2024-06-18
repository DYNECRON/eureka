from fastapi import FastAPI
from modules.load_data import load_data_to_dataframe
from fastapi.middleware.cors import CORSMiddleware
from modules.Corpus import Corpus
from modules.retrieve_relevant_docs import retrieve_relevant_docs
from fastapi.encoders import jsonable_encoder
from nltk.stem import WordNetLemmatizer
from modules.metrics import get_metrics

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

df = load_data_to_dataframe()
corpus = Corpus(df)
lemmatizer = WordNetLemmatizer()


@app.get("/{query}")
async def read_item(query: str):
    lemmatizedQuery = lemmatizer.lemmatize(query)
    jaccard_time = corpus.jaccard(query=lemmatizedQuery)
    cosine_time = corpus.cosine(query=lemmatizedQuery)

    jaccard, cosine = retrieve_relevant_docs(
        df, corpus.sorted_indices_jacc, corpus.jaccard_similarities,
        corpus.sorted_indices_cos, corpus.cosine_distances)

    jaccard_recall, jaccard_precision, jaccard_f1_score = get_metrics(
        query, corpus.best_titles_jaccard)

    cosine_recall, cosine_precision, cosine_f1_score = get_metrics(
        query, corpus.best_titles_cosine)

    result = {
        "jaccard": jaccard, "jaccard_time": jaccard_time,
        "jaccard_recall": jaccard_recall, "jaccard_precision": jaccard_precision,
        "jaccard_f1_score": jaccard_f1_score,
        "cosine": cosine, "cosine_time": cosine_time,
        "cosine_recall": cosine_recall, "cosine_precision": cosine_precision,
        "cosine_f1_score": cosine_f1_score,
    }

    json_result = jsonable_encoder(result)
    return json_result
