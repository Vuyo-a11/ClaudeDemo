"""Movie Detail App - Search and display detailed information about movies using TMDB API."""

import streamlit as st
from config import APP_TITLE
from api import (
    validate_api_key, search_movies, get_movie_details, get_movie_credits,
    get_recommendations, get_videos, get_reviews, get_trending_movies, 
    get_top_rated_movies, get_person_details, get_person_filmography
)
from utils import (
    build_search_options, display_movie_details, display_cast_and_crew,
    display_trailers, display_reviews, display_recommendations,
    display_trending_or_top_section, display_favorites_section,
    display_watchlist_section, display_movie_action_buttons,
    display_actor_filmography, display_movie_comparison
)


def initialize_session_state() -> None:
    """Initialize Streamlit session state variables."""
    if "selected_movie_id" not in st.session_state:
        st.session_state.selected_movie_id = None
    if "search_results" not in st.session_state:
        st.session_state.search_results = {}
    if "show_trending" not in st.session_state:
        st.session_state.show_trending = True
    if "view_mode" not in st.session_state:
        st.session_state.view_mode = "search"  # search, favorites, watchlist, compare, actor, settings
    if "comparison_movies" not in st.session_state:
        st.session_state.comparison_movies = []
    if "compare_results" not in st.session_state:
        st.session_state.compare_results = {}


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


def render_sidebar() -> None:
    """Render sidebar navigation."""
    st.sidebar.title("🎬 Navigation")
    
    view = st.sidebar.radio(
        "Choose View:",
        ["🔍 Search", "❤️ Favorites", "📋 Watchlist", "👥 Compare Movies", "🌟 Actor", "Settings"],
        key="nav_radio"
    )
    
    if view == "🔍 Search":
        st.session_state.view_mode = "search"
    elif view == "❤️ Favorites":
        st.session_state.view_mode = "favorites"
    elif view == "📋 Watchlist":
        st.session_state.view_mode = "watchlist"
    elif view == "👥 Compare Movies":
        st.session_state.view_mode = "compare"
    elif view == "🌟 Actor":
        st.session_state.view_mode = "actor"
    elif view == "Settings":
        st.session_state.view_mode = "settings"
    
    st.sidebar.divider()
    st.sidebar.markdown("**Built with TMDB API**")


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
        
        # Action buttons (Favorites & Watchlist)
        display_movie_action_buttons(movie_details)
        
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
        initial_sidebar_state="expanded"
    )
    
    # Validate API key
    if not validate_api_key():
        st.stop()
    
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar navigation
    render_sidebar()
    
    # Render app based on view mode
    if st.session_state.view_mode == "search":
        st.title(APP_TITLE)
        st.markdown("Search for movies and discover detailed information from **The Movie Database (TMDB)**")
        
        render_search_section()
        render_selection_section()
        render_details_section()
        render_discovery_section()
    
    elif st.session_state.view_mode == "favorites":
        st.title("❤️ My Favorite Movies")
        display_favorites_section()
    
    elif st.session_state.view_mode == "watchlist":
        st.title("📋 My Watchlist")
        display_watchlist_section()
    
    elif st.session_state.view_mode == "compare":
        st.title("👥 Compare Movies")
        st.markdown("Search for movies and add them to compare side-by-side")
        
        if "comparison_movies" not in st.session_state:
            st.session_state.comparison_movies = []
        
        col1, col2 = st.columns([3, 1])
        with col1:
            query = st.text_input("Search for movies to compare", placeholder="e.g., Inception")
        with col2:
            if st.button("Search", use_container_width=True):
                results = search_movies(query)
                if results:
                    st.session_state.compare_results = build_search_options(results)
                    st.success(f"Found {len(results)} movies")
        
        if hasattr(st.session_state, 'compare_results') and st.session_state.compare_results:
            choice = st.selectbox("Add to comparison:", list(st.session_state.compare_results.keys()))
            if st.button("Add Movie to Compare"):
                movie_id = st.session_state.compare_results[choice]
                movie = get_movie_details(movie_id)
                if movie:
                    # Check if already in comparison
                    if not any(m.get('id') == movie_id for m in st.session_state.comparison_movies):
                        st.session_state.comparison_movies.append(movie)
                        st.success(f"Added {movie.get('title')} to comparison")
                    else:
                        st.warning("Movie already in comparison")
        
        if st.session_state.comparison_movies:
            st.write(f"**Comparing {len(st.session_state.comparison_movies)} movies:**")
            cols = st.columns(len(st.session_state.comparison_movies))
            for col, movie in zip(cols, st.session_state.comparison_movies):
                with col:
                    st.write(f"**{movie.get('title')}**")
                    if st.button("Remove", key=f"remove_{movie.get('id')}"):
                        st.session_state.comparison_movies = [m for m in st.session_state.comparison_movies if m.get('id') != movie.get('id')]
                        st.rerun()
            
            st.divider()
            display_movie_comparison(st.session_state.comparison_movies)
    
    elif st.session_state.view_mode == "actor":
        st.title("🌟 Actor & Director Filmography")
        st.markdown("Search for actors and discover their filmography")
        
        query = st.text_input("Search for actor/director name", placeholder="e.g., Tom Hanks")
        
        if query:
            results = search_movies(query.split()[0])  # Use first word to search for movies with that actor
            
            # Extract unique cast members from results
            all_cast = set()
            for movie in results:
                movie_details = get_movie_details(movie.get('id'))
                if movie_details:
                    credits = movie_details.get('credits', {})
                    for cast_member in credits.get('cast', [])[:5]:
                        all_cast.add((cast_member.get('name'), cast_member.get('id')))
            
            if all_cast:
                actor_choice = st.selectbox(
                    "Select an actor/director:",
                    options=sorted(all_cast, key=lambda x: x[0]),
                    format_func=lambda x: x[0]
                )
                
                if actor_choice:
                    actor_name, person_id = actor_choice
                    display_actor_filmography(person_id, actor_name)
            else:
                st.info(f"No cast information found for '{query}'")
    
    elif st.session_state.view_mode == "settings":
        st.title("⚙️ Settings")
        st.markdown("App settings and information")
        
        st.subheader("About")
        st.info("""
        **Movie Detail App**
        
        A comprehensive movie database application powered by **The Movie Database (TMDB) API**.
        
        Features:
        - 🔍 Search for movies
        - ❤️ Save favorite movies
        - 📋 Create watchlists
        - 👥 Compare movies side-by-side
        - 🌟 Browse actor filmography
        - 📄 Export movie details as PDF
        """)
        
        st.subheader("Storage Info")
        st.markdown("Your data is stored locally in: `~/.movie_app/`")
        
        if st.button("Clear All Local Data", type="secondary"):
            from storage import STORAGE_DIR
            import shutil
            try:
                shutil.rmtree(STORAGE_DIR)
                st.success("All local data cleared!")
                st.rerun()
            except Exception as e:
                st.error(f"Could not clear data: {str(e)}")


if __name__ == "__main__":
    main()

