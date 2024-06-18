import numpy as np
import re
titulos = []


def crear_array_query(query, df):
    nombres_columnas = df.columns.tolist()
    patrones = [r'\b{}\b'.format(re.escape(palabra))
                for palabra in query.split()]
    regex = re.compile('|'.join(patrones))
    resultado = [1 if regex.search(
        columna) else 0 for columna in nombres_columnas]
    return resultado


def similitud_jaccard(query, text, scores):
    interseccion = np.sum(np.logical_and(query, text))
    union = np.sum(np.logical_or(query, text))
    jaccard_score = interseccion / union if union != 0 else 0.0
    scores.append(jaccard_score)


def calculo_distancia(np_array_query, np_array_text, scores):
    producto_punto = np.dot(np_array_query, np_array_text)

    norma_a = np.linalg.norm(np_array_query)
    norma_b = np.linalg.norm(np_array_text)

    distancia_coseno = producto_punto / (norma_a * norma_b)
    scores.append(distancia_coseno)


def ranked_skores(scores, df):
    score_sorted = sorted(scores, reverse=True)
    # best_scores=score_sorted[:3]
    best_titles = []
    titulos = df.index.tolist()
    titulos_aux = titulos.copy()
    contador = 0
    for score in score_sorted:
        if score > 0:
            indice = scores.index(score)
            best_titles.append(titulos[indice])
            scores[indice] = None
            titulos_aux[indice] = None
    return best_titles


def process_query_jaccard(query, df):
    array_query = np.array(crear_array_query(query, df))
    print("Query a procesar: ", query)
    scores_jaccard = []
    socores_coss = []
    for ind, fil in df.iterrows():
        array_doc = np.array(fil)
        similitud_jaccard(array_query, array_doc, scores_jaccard)
        calculo_distancia(array_query, array_doc, socores_coss)
    best_titles_jacc = ranked_skores(scores_jaccard, df)
    best_titles_cos = ranked_skores(socores_coss, df)
    return best_titles_jacc, best_titles_cos
