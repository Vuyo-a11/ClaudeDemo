"""TMDB API client module."""

import requests
import streamlit as st
from typing import Any, Dict, List, Optional
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


@st.cache_data(ttl=CACHE_TTL)
def get_genre_list() -> List[Dict]:
    """Fetch list of available movie genres from TMDB.

    Returns:
        List of genre dictionaries with id and name
    """
    try:
        params = {"api_key": API_KEY}
        response = requests.get(f"{BASE_URL}/genre/movie/list", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("genres", [])
    except requests.RequestException as e:
        st.warning(f"⚠️ Could not load genres: {str(e)}")
        return []


@st.cache_data(ttl=CACHE_TTL)
def get_language_list() -> List[Dict]:
    """Fetch supported language codes from TMDB.

    Returns:
        List of language dictionaries containing iso_639_1 and english_name.
    """
    try:
        params = {"api_key": API_KEY}
        response = requests.get(f"{BASE_URL}/configuration/languages", params=params, timeout=10)
        response.raise_for_status()
        return response.json()  # this endpoint returns a list
    except requests.RequestException as e:
        st.warning(f"⚠️ Could not load language list: {str(e)}")
        return []


@st.cache_data(ttl=CACHE_TTL)
def search_movies_advanced(
    query: str = "",
    year: Optional[int] = None,
    language: Optional[str] = None,
    genre_id: Optional[int] = None,
    min_rating: Optional[float] = None,
) -> List[Dict]:
    """Perform a movie search with additional filters.

    Args:
        query: Search text (optional). If left empty, the discover endpoint is used.
        year: Primary release year to filter by.
        language: Original language code (iso_639_1).
        genre_id: TMDB genre id.
        min_rating: Minimum vote average to include.

    Returns:
        Filtered list of movie dictionaries.
    """
    results: List[Dict] = []

    # If the user provided a query, start with standard search
    if query:
        results = search_movies(query)
    else:
        # Use discover endpoint to honor filters even without query
        try:
            params: Dict[str, Any] = {"api_key": API_KEY}
            if year:
                params["primary_release_year"] = year
            if language:
                params["with_original_language"] = language
            if genre_id:
                params["with_genres"] = genre_id
            if min_rating is not None:
                params["vote_average.gte"] = min_rating

            response = requests.get(f"{BASE_URL}/discover/movie", params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
        except requests.RequestException as e:
            st.warning(f"⚠️ Advanced discover failed: {str(e)}")
            results = []

    # apply filters on search results as well
    if query and any([year, language, genre_id, min_rating is not None]):
        filtered = []
        for m in results:
            if year:
                rd = m.get("release_date", "")
                if not rd.startswith(str(year)):
                    continue
            if language and m.get("original_language") != language:
                continue
            if genre_id:
                # search results include ``genre_ids`` list
                if genre_id not in m.get("genre_ids", []):
                    continue
            if min_rating is not None:
                if m.get("vote_average", 0) < min_rating:
                    continue
            filtered.append(m)
        results = filtered

    return results


@st.cache_data(ttl=CACHE_TTL)
def discover_movies_by_genre(genre_id: int) -> List[Dict]:
    """Discover movies filtered by genre using TMDB discover endpoint.

    Args:
        genre_id: numeric genre identifier
    
    Returns:
        List of movie dictionaries matching genre
    """
    try:
        params = {"api_key": API_KEY, "with_genres": genre_id}
        response = requests.get(f"{BASE_URL}/discover/movie", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.RequestException as e:
        st.warning(f"⚠️ Could not discover movies: {str(e)}")
        return []


@st.cache_data(ttl=CACHE_TTL)
def get_person_details(person_id: int) -> Optional[Dict]:
    """Fetch person (actor/director) details.
    
    Args:
        person_id: TMDB person ID
        
    Returns:
        Person details dictionary
    """
    try:
        params = {"api_key": API_KEY}
        response = requests.get(f"{BASE_URL}/person/{person_id}", params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.warning(f"⚠️ Could not load person details: {str(e)}")
        return None


@st.cache_data(ttl=CACHE_TTL)
def get_person_filmography(person_id: int) -> List[Dict]:
    """Fetch filmography for a person (actor/director).
    
    Args:
        person_id: TMDB person ID
        
    Returns:
        List of movie dictionaries
    """
    try:
        params = {"api_key": API_KEY}
        response = requests.get(f"{BASE_URL}/person/{person_id}/movie_credits", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Return cast movies, sorted by release date
        cast = data.get("cast", [])
        return sorted(cast, key=lambda x: x.get("release_date", ""), reverse=True)
    except requests.RequestException as e:
        st.warning(f"⚠️ Could not load filmography: {str(e)}")
        return []
