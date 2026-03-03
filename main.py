"""Movie Detail App - Search and display detailed information about movies using TMDB API."""

import streamlit as st
from config import APP_TITLE
from api import (
    validate_api_key, search_movies, get_movie_details, get_movie_credits,
    get_recommendations, get_videos, get_reviews, get_trending_movies, 
    get_top_rated_movies
)
from utils import (
    build_search_options, display_movie_details, display_cast_and_crew,
    display_trailers, display_reviews, display_recommendations,
    display_trending_or_top_section
)


def initialize_session_state() -> None:
    """Initialize Streamlit session state variables."""
    if "selected_movie_id" not in st.session_state:
        st.session_state.selected_movie_id = None
    if "search_results" not in st.session_state:
        st.session_state.search_results = {}
    if "show_trending" not in st.session_state:
        st.session_state.show_trending = True


def handle_search(query: str) -> None:
    """Handle movie search and update session state.
    
    Args:
        query: Search query string
    """
    if not query.strip():
        st.warning("⚠️ Please enter a search query")
        return
    
    with st.spinner("🔍 Searching movies..."):
        results = search_movies(query)
    
    if results:
        st.session_state.search_results = build_search_options(results)
        st.session_state.show_trending = False
        st.success(f"✅ Found {len(results)} movies")
    else:
        st.warning("⚠️ No movies found. Try a different search term.")
        st.session_state.search_results = {}


def render_search_section() -> None:
    """Render the search input section."""
    st.subheader("🎬 Search for a Movie")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("Movie title", key="search_input", placeholder="e.g., The Matrix")
    with col2:
        if st.button("Search", use_container_width=True):
            handle_search(query)


def render_selection_section() -> None:
    """Render the movie selection dropdown."""
    if not st.session_state.search_results:
        return
    
    st.subheader("🎥 Select a Movie")
    choice = st.selectbox(
        "Choose from results:",
        options=[""] + list(st.session_state.search_results.keys()),
        format_func=lambda x: x if x else "-- Select a movie --"
    )
    
    if choice and choice != "":
        st.session_state.selected_movie_id = st.session_state.search_results[choice]


def render_details_section() -> None:
    """Render the movie details display with all content & discovery features."""
    if not st.session_state.selected_movie_id:
        return
    
    movie_details = get_movie_details(st.session_state.selected_movie_id)
    
    if movie_details:
        st.divider()
        
        # Main movie details
        display_movie_details(movie_details)
        
        st.divider()
        
        # Cast and crew
        credits = get_movie_credits(st.session_state.selected_movie_id)
        display_cast_and_crew(credits)
        
        st.divider()
        
        # Videos/Trailers
        videos = get_videos(st.session_state.selected_movie_id)
        display_trailers(videos)
        
        st.divider()
        
        # Reviews
        reviews = get_reviews(st.session_state.selected_movie_id)
        display_reviews(reviews)
        
        st.divider()
        
        # Recommendations
        recommendations = get_recommendations(st.session_state.selected_movie_id)
        display_recommendations(recommendations)


def render_discovery_section() -> None:
    """Render trending and top-rated sections."""
    if not st.session_state.show_trending:
        return
    
    st.divider()
    st.subheader("🔥 Discover Movies")
    
    tab1, tab2 = st.tabs(["📈 Trending This Week", "🏆 Top Rated"])
    
    with tab1:
        with st.spinner("Loading trending movies..."):
            trending = get_trending_movies()
        display_trending_or_top_section("Trending This Week", trending)
    
    with tab2:
        with st.spinner("Loading top-rated movies..."):
            top_rated = get_top_rated_movies()
        display_trending_or_top_section("Top Rated Movies", top_rated)


def main() -> None:
    """Main application entry point."""
    # Page configuration
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Validate API key
    if not validate_api_key():
        st.stop()
    
    # Initialize session state
    initialize_session_state()
    
    # Render app
    st.title(APP_TITLE)
    st.markdown("Search for movies and discover detailed information from **The Movie Database (TMDB)**")
    
    render_search_section()
    render_selection_section()
    render_details_section()
    render_discovery_section()


if __name__ == "__main__":
    main()

