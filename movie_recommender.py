import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast

class MovieRecommender:
    def __init__(self):
        self.movies_df = None
        self.cosine_sim = None
        self.indices = None
        
    def load_data(self, movies_path):
        self.movies_df = pd.read_csv(movies_path)
        print(f"Loaded {len(self.movies_df)} movies")
        return self.movies_df
    
    def preprocess_data(self):
        # Handle missing values
        self.movies_df = self.movies_df.dropna(subset=['overview', 'genres'])
        
        # Convert stringified lists to actual lists
        self.movies_df['genres'] = self.movies_df['genres'].apply(self._extract_names)
        
        # Create a combined feature for recommendation
        self.movies_df['combined_features'] = (
            self.movies_df['overview'] + ' ' +
            self.movies_df['genres'].apply(lambda x: ' '.join(x))
        )
        
        return self.movies_df
    
    def _extract_names(self, x):
        try:
            if pd.isna(x):
                return []
            lst = ast.literal_eval(x)
            return [item['name'] for item in lst] if isinstance(lst, list) else []
        except:
            return []
    
    def build_model(self):
        # Create TF-IDF matrix
        tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
        tfidf_matrix = tfidf.fit_transform(self.movies_df['combined_features'])
        
        # Compute cosine similarity matrix
        self.cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        
        # Create mapping from title to index
        self.indices = pd.Series(
            self.movies_df.index, 
            index=self.movies_df['title']
        ).drop_duplicates()
        
    def get_recommendations(self, title, num_recommendations=10):
        if title not in self.indices:
            return None
        
        # Get the index of the movie
        idx = self.indices[title]
        
        # Get pairwise similarity scores
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        
        # Sort movies based on similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get scores of the most similar movies
        sim_scores = sim_scores[1:num_recommendations+1]
        
        # Get movie indices
        movie_indices = [i[0] for i in sim_scores]
        similarity_scores = [i[1] for i in sim_scores]
        
        # Return the top most similar movies
        recommendations = self.movies_df.iloc[movie_indices].copy()
        recommendations['similarity_score'] = similarity_scores
        
        return recommendations[['title', 'genres', 'vote_average', 'vote_count', 'similarity_score']]
    
    def search_movies(self, search_term):
        return self.movies_df[
            self.movies_df['title'].str.contains(search_term, case=False)
        ]['title'].tolist()