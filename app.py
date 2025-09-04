import streamlit as st
from movie_recommender import MovieRecommender
import time

# Initialize the recommender system
@st.cache_resource
def load_recommender():
    recommender = MovieRecommender()
    movies_df = recommender.load_data("tmdb_5000_movies.csv")
    movies_clean = recommender.preprocess_data()
    recommender.build_model()
    return recommender

def main():
    st.title("Movie Recommendation System")
    st.write("Enter a movie you like and get similar recommendations!")
    
    # Load data and model
    with st.spinner("Loading movie data..."):
        recommender = load_recommender()
    
    # Input field for movie search
    st.header("Find Movie Recommendations")
    
    # Search input with autocomplete
    search_term = st.text_input(
        "Type a movie title:",
        placeholder="Start typing to see suggestions...",
        key="movie_search"
    )
    
    # Show search suggestions as user types
    if search_term and len(search_term) > 2:
        suggestions = recommender.search_movies(search_term)
        if suggestions:
            st.write("**Suggestions:**")
            for suggestion in suggestions[:5]:  # Show top 5 suggestions
                if st.button(suggestion, key=suggestion):
                    st.session_state.selected_movie = suggestion
        else:
            st.info("No movies found. Try a different search term.")
    
    # Selected movie display
    if 'selected_movie' in st.session_state:
        st.success(f"Selected: **{st.session_state.selected_movie}**")
    
    # Number of recommendations slider
    num_recommendations = st.slider(
        "Number of recommendations:",
        min_value=5,
        max_value=20,
        value=10,
        key="num_recs"
    )
    
    # Get recommendations button
    if st.button("Get Recommendations", type="primary"):
        if 'selected_movie' in st.session_state:
            with st.spinner(f"Finding movies similar to '{st.session_state.selected_movie}'..."):
                recommendations = recommender.get_recommendations(
                    st.session_state.selected_movie, 
                    num_recommendations
                )
                
                if recommendations is not None and not recommendations.empty:
                    st.success("🎉 Here are your movie recommendations!")
                    
                    # Display recommendations in a grid
                    cols = st.columns(2)
                    for i, (idx, row) in enumerate(recommendations.iterrows()):
                        with cols[i % 2]:
                            with st.container():
                                st.subheader(f"{i+1}. {row['title']}")
                                
                                # Display genres
                                genres = ", ".join(row['genres']) if isinstance(row['genres'], list) else row['genres']
                                st.write(f"**Genres:** {genres}")
                                
                                # Rating and votes
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.metric("Rating", f"{row['vote_average']}/10")
                                with col2:
                                    st.metric("Votes", f"{row['vote_count']}")
                                
                                # Similarity score with progress bar
                                similarity_percent = row['similarity_score'] * 100
                                st.write(f"**Similarity:** {similarity_percent:.1f}%")
                                st.progress(row['similarity_score'])
                                
                                st.markdown("---")
                else:
                    st.error("No recommendations found. Please try another movie.")
        else:
            st.warning("Please select a movie first!")

if __name__ == "__main__":
    main()