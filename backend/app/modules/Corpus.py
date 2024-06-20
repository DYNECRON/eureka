from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import numpy as np
import time


class Corpus:
    def __init__(self, data_frame):
        self.count_vectorizer = CountVectorizer(binary=True)
        self.tfidf_vectorizer = TfidfVectorizer()
        self.df = data_frame
        self.bag_of_words_matrix = self.create_bag_of_words()
        self.tfidf_matrix = self.create_tf_idf()
        self.best_titles_jaccard = None
        self.best_titles_cosine = None
        self.sorted_indices_jacc = None
        self.sorted_indices_cos = None
        self.jaccard_similarities = None
        self.cosine_distances = None

    def create_bag_of_words(self):
        bow_matrix = self.count_vectorizer.fit_transform(
            self.df['processed_text'])
        return bow_matrix

    def create_tf_idf(self):
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(
            self.df['processed_text'])
        return tfidf_matrix

    def jaccard(self, query):
        print("procesando jaccard.....")
        start = time.time()
        query_vector = self.count_vectorizer.transform([query])
        self.jaccard_similarities = []
        for idx in range(self.bag_of_words_matrix.shape[0]):
            a = query_vector.toarray().squeeze()
            b = self.bag_of_words_matrix[idx].toarray().squeeze()
            intersection = np.sum(np.logical_and(a, b))
            union = np.sum(np.logical_or(a, b))
            similarity = intersection/union if union != 0 else 0.0
            self.jaccard_similarities.append(similarity)

        sorted_indices = np.argsort(self.jaccard_similarities)[::-1]
        self.best_titles_jaccard = []
        self.sorted_indices_jacc = sorted_indices
        for idx in (sorted_indices):
            if (self.jaccard_similarities[idx] > 0.0):
                filename = self.df['filename'].iloc[idx]
                self.best_titles_jaccard.append(filename)
            else:
                break
        end = time.time()
        time_taken_ms = round((end-start) * 1000)
        print("Finalizó jaccard Time in ms: ", time_taken_ms)
        return time_taken_ms

    def cosine(self, query):
        print("procesando cosine.....")
        start = time.time()
        query_tfidf_vector = self.tfidf_vectorizer.transform([query])
        self.cosine_distances = []
        for idx in range(self.tfidf_matrix.shape[0]):
            a = self.tfidf_matrix[idx].toarray().squeeze()
            b = query_tfidf_vector.toarray().squeeze()
            if np.linalg.norm(a)*np.linalg.norm(b) > 0.0:
                cos_distance = np.dot(
                    a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
            else:
                cos_distance = 0.0
            self.cosine_distances.append(cos_distance)

        sorted_indices = np.argsort(self.cosine_distances)[::-1]
        self.best_titles_cosine = []
        self.sorted_indices_cos = sorted_indices
        for idx in (sorted_indices):
            if (self.cosine_distances[idx] > 0.0):
                filename = self.df['filename'].iloc[idx]
                self.best_titles_cosine.append(filename)
            else:
                break
        end = time.time()
        time_taken_ms = round((end-start) * 1000)
        print("Finalizó cosine Time in ms: ", time_taken_ms)
        return time_taken_ms
