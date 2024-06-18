from modules.Result import Result


def retrieve_relevant_docs(df, sorted_indices, jaccard_sim, sorted_indices_cos, cosine_distances):

    result_jacc = []
    result_cosine = []

    print("Recuperando archivos")
    for idx in sorted_indices:
        if (jaccard_sim[idx] > 0):
            filename = df['filename'].iloc[idx]
            texto = df['original_text'].iloc[idx]
            result_jacc.append(Result(filename, texto))
        else:
            break

    for idx in sorted_indices_cos:
        if (cosine_distances[idx] > 0):
            filename = df['filename'].iloc[idx]
            texto = df['original_text'].iloc[idx]
            result_cosine.append(Result(filename, texto))
        else:
            break

    return result_jacc, result_cosine
