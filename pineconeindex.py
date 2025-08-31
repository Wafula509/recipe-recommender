# Remove these installation commands as they're not needed in the Streamlit app
# !pip install sentence-transformers
# !pip install pinecone-client
# !pip install tensorflow

import json
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

# Initialize the sentence transformer model
model = SentenceTransformer('all-MPNet-base-v2')

# Define weights for each column (0 to 1)
weights = {
    "recipe_name": 0.8,
    "cuisine": 0.8,
    "ingredients": 0.8,
    "prep_time": 0.5,
    "mood_tags": 1,
    "time_tags": 0.7,
    "season_tags": 0.8,
    "description": 0.5,
}

# Function to concatenate relevant columns into a single weighted text field
def concatenate_weighted_text(row):
    weighted_text = ""
    for col, weight in weights.items():
        if col in row and pd.notna(row[col]):
            text = str(row[col])
            # Add text multiple times based on weight
            weighted_text += (text + ' ') * int(weight * 10)
    return weighted_text.strip()

class LocalVectorIndex:
    def __init__(self, index_name="recipe_index"):
        self.index_name = index_name
        self.vectors = None
        self.metadata = None
        self.ids = None
        
    def upsert(self, vectors):
        """Store vectors and metadata locally"""
        self.ids = [v[0] for v in vectors]
        self.vectors = np.array([v[1] for v in vectors])
        self.metadata = [v[2] for v in vectors]
        
    def query(self, vector, top_k=5):
        """Query the local index for similar vectors"""
        if self.vectors is None:
            return []
            
        # Calculate cosine similarity
        similarities = cosine_similarity([vector], self.vectors)[0]
        
        # Get top_k most similar items
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Prepare results in Pinecone-like format
        results = []
        for idx in top_indices:
            results.append({
                "id": self.ids[idx],
                "score": similarities[idx],
                "metadata": self.metadata[idx]
            })
            
        return results
    
    def save(self, filepath):
        """Save the index to a file"""
        with open(filepath, 'wb') as f:
            pickle.dump({
                'ids': self.ids,
                'vectors': self.vectors,
                'metadata': self.metadata
            }, f)
    
    def load(self, filepath):
        """Load the index from a file"""
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
                self.ids = data['ids']
                self.vectors = data['vectors']
                self.metadata = data['metadata']
        return self

# Initialize local index instead of Pinecone
index_name = "recipe_index"
index = LocalVectorIndex(index_name)

# Check if we have a saved index
saved_index_path = f"{index_name}.pkl"
if os.path.exists(saved_index_path):
    index.load(saved_index_path)
    print("Loaded existing index from file")
else:
    # Sample data - in a real application, you would load your actual recipe data
    sample_data = {
        "recipe_name": ["Summer Berry Salad", "Hearty Winter Stew", "Spring Vegetable Pasta"],
        "cuisine": ["American", "American", "Italian"],
        "ingredients": [
            "Mixed greens, strawberries, blueberries, feta cheese, walnuts, balsamic vinaigrette",
            "Beef chuck, potatoes, carrots, onions, beef broth, herbs",
            "Pasta, asparagus, peas, lemon, garlic, parmesan cheese"
        ],
        "prep_time": ["15 minutes", "2 hours", "30 minutes"],
        "mood_tags": ["Refreshing", "Comforting", "Energizing"],
        "time_tags": ["Quick", "Slow-cooked", "Moderate"],
        "season_tags": ["Summer", "Winter", "Spring"],
        "description": [
            "A light and refreshing salad perfect for hot summer days",
            "A warm and comforting stew for cold winter nights",
            "A fresh pasta dish with seasonal spring vegetables"
        ]
    }
    
    df = pd.DataFrame(sample_data)
    
    # Create a combined weighted text field for embedding
    df['combined_weighted_text'] = df.apply(concatenate_weighted_text, axis=1)

    # Encode the text to get embeddings
    embeddings = model.encode(df['combined_weighted_text'].tolist())

    # Prepare the data for upsert
    vector_data = []
    for i, embedding in enumerate(embeddings):
        # Handle potential NaN values
        recipe_name = df['recipe_name'][i] if pd.notna(df['recipe_name'][i]) else ''
        cuisine = df['cuisine'][i] if pd.notna(df['cuisine'][i]) else ''
        ingredients = df['ingredients'][i] if pd.notna(df['ingredients'][i]) else ''
        prep_time = df['prep_time'][i] if pd.notna(df['prep_time'][i]) else ''
        mood_tags = df['mood_tags'][i] if pd.notna(df['mood_tags'][i]) else ''
        time_tags = df['time_tags'][i] if pd.notna(df['time_tags'][i]) else ''
        season_tags = df['season_tags'][i] if pd.notna(df['season_tags'][i]) else ''
        description = df['description'][i] if pd.notna(df['description'][i]) else ''

        metadata = {
            "recipe_name": recipe_name,
            "cuisine": cuisine,
            "ingredients": ingredients,
            "prep_time": prep_time,
            "mood_tags": mood_tags,
            "time_tags": time_tags,
            "season_tags": season_tags,
            "description": description
        }

        vector_data.append((str(i), embedding.tolist(), metadata))

    # Upsert the data to our local index
    index.upsert(vector_data)
    
    # Save the index for future use
    index.save(saved_index_path)
    
    print("Recipe data uploaded to local index successfully!")

# Function to query the local index
def query_recipes(user_input, top_k=5):
    """
    Query recipes based on user input
    user_input: dict with keys like mood, cuisine, season, etc.
    """
    # Create a query string from user input
    query_text = ""
    for key, value in user_input.items():
        if value:  # Only add non-empty values
            weight = weights.get(key, 0.5)
            query_text += (str(value) + ' ') * int(weight * 10)
    
    # Generate embedding for the query
    query_embedding = model.encode([query_text])[0]
    
    # Query the local index
    results = index.query(query_embedding, top_k=top_k)
    
    return results

# Example usage:
if __name__ == "__main__":
    # Example query
    user_preferences = {
        "mood_tags": "Comforting",
        "cuisine": "American",
        "season_tags": "Winter"
    }
    
    similar_recipes = query_recipes(user_preferences)
    print("Similar recipes found:")
    for recipe in similar_recipes:
        print(f"- {recipe['metadata']['recipe_name']} (Score: {recipe['score']:.3f})")