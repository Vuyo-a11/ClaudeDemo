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


def display_cast_and_crew(credits: Dict) -> None:
    """Display cast and crew members.
    
    Args:
        credits: Credits dictionary from API
    """
    st.subheader("👥 Cast & Crew")
    
    cast = credits.get("cast", [])[:10]  # Show top 10 cast members
    
    if cast:
        cols = st.columns(min(5, len(cast)))
        for idx, actor in enumerate(cast):
            with cols[idx % len(cols)]:
                st.write(f"**{actor.get('name', 'Unknown')}**")
                if actor.get("profile_path"):
                    st.image(f"{IMAGE_BASE_URL}{actor.get('profile_path')}")
                st.caption(actor.get("character", "Unknown role"))
    else:
        st.info("No cast information available")


def display_trailers(videos: List[Dict]) -> None:
    """Display trailers and videos.
    
    Args:
        videos: List of video dictionaries from API
    """
    trailers = [v for v in videos if v.get("type") in ["Trailer", "Teaser", "Clip"]]
    
    if not trailers:
        return
    
    st.subheader("🎬 Trailers & Videos")
    
    for video in trailers[:3]:  # Show up to 3 videos
        if video.get("site") == "YouTube":
            video_key = video.get("key")
            st.video(f"https://www.youtube.com/watch?v={video_key}")
            st.caption(f"{video.get('type')}: {video.get('name', 'Video')}")


def display_reviews(reviews: List[Dict]) -> None:
    """Display movie reviews.
    
    Args:
        reviews: List of review dictionaries from API
    """
    if not reviews:
        return
    
    st.subheader("📖 Reviews")
    
    for review in reviews[:5]:  # Show up to 5 reviews
        with st.expander(f"⭐ Review by {review.get('author', 'Anonymous')} ({review.get('author_details', {}).get('rating', 'N/A')}/10)"):
            st.write(review.get("content", "No content available"))
            st.caption(f"*{review.get('created_at', 'N/A')[:10]}*")


def display_recommendations(recommendations: List[Dict]) -> None:
    """Display recommended movies.
    
    Args:
        recommendations: List of movie dictionaries from API
    """
    if not recommendations:
        return
    
    st.subheader("🎯 Recommended Movies")
    
    cols = st.columns(5)
    for idx, movie in enumerate(recommendations[:10]):
        with cols[idx % 5]:
            st.write(f"**{movie.get('title', 'Unknown')[:15]}...**")
            if movie.get("poster_path"):
                st.image(f"{IMAGE_BASE_URL}{movie.get('poster_path')}")
            st.caption(f"⭐ {movie.get('vote_average', 'N/A')}")


def display_trending_or_top_section(title: str, movies: List[Dict]) -> None:
    """Display trending or top-rated movies.
    
    Args:
        title: Section title
        movies: List of movie dictionaries
    """
    if not movies:
        return
    
    st.subheader(title)
    
    cols = st.columns(5)
    for idx, movie in enumerate(movies[:10]):
        with cols[idx % 5]:
            st.write(f"**{movie.get('title', 'Unknown')[:15]}...**")
            if movie.get("poster_path"):
                st.image(f"{IMAGE_BASE_URL}{movie.get('poster_path')}")
            st.caption(f"⭐ {movie.get('vote_average', 'N/A')}")
