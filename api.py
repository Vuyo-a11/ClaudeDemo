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


@st.cache_data(ttl=CACHE_TTL)
def get_movie_credits(movie_id: int) -> Dict:
    """Fetch cast and crew information for a movie.
    
    Args:
        movie_id: TMDB movie ID
        
    Returns:
        Credits dictionary with cast and crew
    """
    try:
        params = {"api_key": API_KEY}
        response = requests.get(f"{BASE_URL}/movie/{movie_id}/credits", params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.warning(f"⚠️ Could not load cast information: {str(e)}")
        return {"cast": [], "crew": []}


@st.cache_data(ttl=CACHE_TTL)
def get_recommendations(movie_id: int) -> List[Dict]:
    """Fetch recommended movies similar to the given movie.
    
    Args:
        movie_id: TMDB movie ID
        
    Returns:
        List of recommended movies
    """
    try:
        params = {"api_key": API_KEY}
        response = requests.get(f"{BASE_URL}/movie/{movie_id}/recommendations", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.RequestException as e:
        st.warning(f"⚠️ Could not load recommendations: {str(e)}")
        return []


@st.cache_data(ttl=CACHE_TTL)
def get_videos(movie_id: int) -> List[Dict]:
    """Fetch trailers and video links for a movie.
    
    Args:
        movie_id: TMDB movie ID
        
    Returns:
        List of video dictionaries with YouTube links
    """
    try:
        params = {"api_key": API_KEY}
        response = requests.get(f"{BASE_URL}/movie/{movie_id}/videos", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.RequestException as e:
        st.warning(f"⚠️ Could not load videos: {str(e)}")
        return []


@st.cache_data(ttl=CACHE_TTL)
def get_reviews(movie_id: int) -> List[Dict]:
    """Fetch user reviews for a movie.
    
    Args:
        movie_id: TMDB movie ID
        
    Returns:
        List of review dictionaries
    """
    try:
        params = {"api_key": API_KEY}
        response = requests.get(f"{BASE_URL}/movie/{movie_id}/reviews", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.RequestException as e:
        st.warning(f"⚠️ Could not load reviews: {str(e)}")
        return []


@st.cache_data(ttl=CACHE_TTL)
def get_trending_movies() -> List[Dict]:
    """Fetch trending movies for the week.
    
    Returns:
        List of trending movie dictionaries
    """
    try:
        params = {"api_key": API_KEY}
        response = requests.get(f"{BASE_URL}/trending/movie/week", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.RequestException as e:
        st.warning(f"⚠️ Could not load trending movies: {str(e)}")
        return []


@st.cache_data(ttl=CACHE_TTL)
def get_top_rated_movies() -> List[Dict]:
    """Fetch top-rated movies.
    
    Returns:
        List of top-rated movie dictionaries
    """
    try:
        params = {"api_key": API_KEY}
        response = requests.get(f"{BASE_URL}/movie/top_rated", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.RequestException as e:
        st.warning(f"⚠️ Could not load top-rated movies: {str(e)}")
        return []
