from sklearn.feature_extraction.text import TfidfVectorizer

def vectorize_texts(texts):
    return TfidfVectorizer(stop_words="english").fit_transform(texts)
