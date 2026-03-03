"""TMDB API client module."""

import requests
import streamlit as st
from typing import Dict, List, Optional
from config import API_KEY, BASE_URL, CACHE_TTL


def validate_api_key() -> bool:
    """Validate that API key is configured."""
    if not API_KEY:
        st.error("❌ TMDB_API_KEY environment variable not set. Please export your API key before running.")
        return False
    return True


@st.cache_data(ttl=CACHE_TTL)
def search_movies(query: str) -> List[Dict]:
    """Search for movies by query.
    
    Args:
        query: Movie title search string
        
    Returns:
        List of movie dictionaries from API
    """
    try:
        params = {"api_key": API_KEY, "query": query}
        response = requests.get(f"{BASE_URL}/search/movie", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.RequestException as e:
        st.error(f"❌ Failed to search movies: {str(e)}")
        return []


@st.cache_data(ttl=CACHE_TTL)
def get_movie_details(movie_id: int) -> Optional[Dict]:
    """Fetch detailed information for a movie.
    
    Args:
        movie_id: TMDB movie ID
        
    Returns:
        Movie details dictionary or None if request fails
    """
    try:
        params = {"api_key": API_KEY}
        response = requests.get(f"{BASE_URL}/movie/{movie_id}", params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"❌ Failed to fetch movie details: {str(e)}")
        return None
