"""Movie Detail App - Search and display detailed information about movies using TMDB API."""

import streamlit as st
from config import APP_TITLE
from api import validate_api_key, search_movies, get_movie_details
from utils import build_search_options, display_movie_details


def initialize_session_state() -> None:
    """Initialize Streamlit session state variables."""
    if "selected_movie_id" not in st.session_state:
        st.session_state.selected_movie_id = None
    if "search_results" not in st.session_state:
        st.session_state.search_results = {}


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
    """Render the movie details display."""
    if not st.session_state.selected_movie_id:
        return
    
    movie_details = get_movie_details(st.session_state.selected_movie_id)
    
    if movie_details:
        st.divider()
        display_movie_details(movie_details)


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


if __name__ == "__main__":
    main()

