from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import joblib
import pandas as pd
import os
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

# Define FastAPI app
app = FastAPI()

# Serve static files (css, js, images, etc.) from the 'static' folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define a model for input query
class QueryModel(BaseModel):
    text: str
    top_n: int = 5

# Load the trained TF-IDF vectorizer and matrix when the app starts
vectorizer_loaded = joblib.load(os.path.join(os.getcwd(), '..', 'model', 'tfidf_vectorizer.pkl'))
tfidf_matrix_loaded = joblib.load(os.path.join(os.getcwd(), '..', 'model', 'tfidf_matrix.pkl'))
df = pd.read_csv(os.path.join(os.getcwd(), '..', 'data', 'dataset.csv'))

# Serve HTML page when the user accesses the root path
@app.get("/", response_class=HTMLResponse)
async def get_homepage():
    with open(os.path.join(os.getcwd(), 'templates', 'index.html'), "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@app.post("/find_similar_abstracts/")
async def find_similar_abstracts(query: QueryModel):
    query_vec = vectorizer_loaded.transform([query.text.lower()])
    similarities = cosine_similarity(query_vec, tfidf_matrix_loaded).flatten()

    # Print the similarity scores to verify they are correct
    print("Similarities:", similarities)

    if similarities.size > 0:
        similar_idx = similarities.argmax()
        # Get the title, authors, and abstract of the most similar abstract
        most_similar_abstract = df['abstract'].iloc[similar_idx]
        title = df['title'].iloc[similar_idx]
        authors = df['authors'].iloc[similar_idx]

        return {
            "most_similar_abstract": most_similar_abstract,
            "similarity_score": similarities[similar_idx],
            "title": title,
            "authors": authors
        }
    else:
        return {"error": "No similar abstracts found."}

