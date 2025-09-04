
# Movie Recommendation System

A content-based movie recommendation system built with Streamlit and scikit-learn. This application suggests similar movies based on their overviews and genres.




## Demo

Live Demo: []()
# Features

- **Smart Search**: Real-time movie suggestions as you type
- **Content-Based Filtering**: Recommendations based on movie overviews and genres
- **Visual Interface**: Clean, user-friendly Streamlit interface
- **Similarity Scores**: Shows how similar each recommendation is to your chosen movie
- **Movie Details**: Displays genres, ratings, and vote counts




## How It Works

### Recommendation Algorithm
1. **Text Processing**: Combines movie overviews and genres into a single text feature
2. **TF-IDF Vectorization**: Converts text into numerical vectors representing word importance
3. **Cosine Similarity**: Calculates how similar each movie is to every other movie
4. **Content-Based Filtering**: Recommends movies with similar content features

### Technical Stack
- **Frontend**: Streamlit for web interface
- **Data Processing**: Pandas for data manipulation
- **Machine Learning**: scikit-learn for TF-IDF and cosine similarity
- **Text Processing**: Natural language processing techniques
## Installation

1. **Clone or download** the project files
2. **Install required packages**:
   
```bash
  pip install streamlit pandas numpy scikit-learn
```

3. Download the dataset from Kaggle

4. Place the CSV file in the project directory:
```bash
tmdb_5000_movies.csv
```
## Usage/Examples

1. Run the application:
```bash
streamlit run app.py
```

2. Open your browser and go to ```http://localhost:8501```

3. Use the application:
- Type a movie title in the search box
- Click on a suggestion from the dropdown
- Adjust the number of recommendations using the slider
- Click "Get Recommendations" to see similar movies
## File Structure

movie-recommendation-system/

├── app.py

├── movie_recommender.py

├── tmdb_5000_movies.csv

└── requirements.txt

app.py - Streamlit web application

movie_recommender.py - Recommendation engine logic

tmdb_5000_movies - Movie dataset 1 (download from Kaggle)

tmdb_5000_credits - Movie dataset 2 (download from Kaggle)

requirements.txt - Python dependencies
## Dataset Information

The system uses the TMDB 5000 Movie Dataset which contains:
- 5000 movies with detailed metadata
- Movie titles, overviews, genres, ratings, and vote counts\
- The dataset is available on [Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
## How Recommendations Are Generated

1. Data Loading: Loads and cleans the movie dataset
2. Feature Engineering: Combines overview and genre text
3. Vectorization: Converts text to TF-IDF vectors
4. Similarity Calculation: Computes cosine similarity between all movies
5. Recommendation: Finds movies most similar to the user's choice