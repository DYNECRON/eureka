from modules.Result import Result


def retrieve_relevant_docs(df, best_titles_jac, jaccard_sim, best_titles_cos, cosine_distances):

    result_jacc = []
    result_cosine = []
    print(len(best_titles_cos))

    print("Recuperando archivos")
    for value in best_titles_jac:
        # filename = df['filename'].iloc[idx]
        texto = df.loc[df['filename'] == value, 'original_text'].iloc[0]
        result_jacc.append(Result(value, texto))

    for value in best_titles_cos:
        # filename = df['filename'].iloc[idx]
        texto = df.loc[df['filename'] == value, 'original_text'].iloc[0]
        # texto = df['original_text'].iloc[idx]
        result_cosine.append(Result(value, texto))

    return result_jacc, result_cosine
