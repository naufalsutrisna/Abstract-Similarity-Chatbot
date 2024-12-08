# There are 2 model to make the chatbot

1. tfidf_matrix.pkl
Stores the processed text data (e.g., a set of predefined responses or documents). This matrix is used to compare incoming queries with stored responses.

2. tfidf_vectorizer.pkl
Used to convert incoming queries into the same format (TF-IDF vectors) as the responses stored in the TF-IDF matrix so that they can be compared for similarity.