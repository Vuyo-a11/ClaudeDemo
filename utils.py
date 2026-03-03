"""Utility functions for UI rendering."""

import streamlit as st
from typing import Dict, List
from config import IMAGE_BASE_URL


def format_search_option(movie: Dict) -> str:
    """Format movie search result as 'Year | Title'.
    
    Args:
        movie: Movie dictionary from API
        
    Returns:
        Formatted string
    """
    year = movie.get("release_date", "")[:4] if movie.get("release_date") else "N/A"
    title = movie.get("title", "Unknown")
    return f"{year} | {title}"


def build_search_options(movies: List[Dict]) -> Dict[str, int]:
    """Build dropdown options from search results.
    
    Args:
        movies: List of movie dictionaries
        
    Returns:
        Dictionary mapping display string to movie ID
    """
    return {format_search_option(m): m.get("id") for m in movies}


def display_movie_details(movie: Dict) -> None:
    """Display formatted movie detail information.
    
    Args:
        movie: Movie details dictionary from API
    """
    # Header with title
    st.header(movie.get("title", "Unknown Title"))
    
    # Poster image
    if movie.get("poster_path"):
        st.image(f"{IMAGE_BASE_URL}{movie.get('poster_path')}", width=200)
    
    # Details in columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Info")
        st.write("**Release Date:**", movie.get("release_date", "N/A"))
        st.write("**Runtime:**", f"{movie.get('runtime', 'N/A')} minutes")
        st.write("**Status:**", movie.get("status", "N/A"))
        st.write("**Language:**", movie.get("original_language", "N/A").upper())
    
    with col2:
        st.subheader("⭐ Ratings & Popularity")
        st.write("**Rating:**", f"{movie.get('vote_average', 'N/A')} / 10")
        st.write("**Popularity:**", f"{movie.get('popularity', 'N/A')}")
        st.write("**Vote Count:**", movie.get("vote_count", "N/A"))
    
    # Overview
    st.subheader("📝 Overview")
    st.write(movie.get("overview", "No overview available"))
    
    # Genres
    genres = movie.get("genres", [])
    if genres:
        genre_names = ", ".join([g["name"] for g in genres])
        st.write("**Genres:**", genre_names)
    
    # Financial info
    budget = movie.get("budget")
    revenue = movie.get("revenue")
    if budget or revenue:
        st.subheader("💰 Financial Info")
        if budget:
            st.write("**Budget:**", f"${budget:,.0f}" if budget > 0 else "N/A")
        if revenue:
            st.write("**Revenue:**", f"${revenue:,.0f}" if revenue > 0 else "N/A")
