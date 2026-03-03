"""Utility functions for UI rendering."""

import streamlit as st
from typing import Dict, List
from config import IMAGE_BASE_URL
from storage import (
    is_favorited, is_in_watchlist, add_to_favorites, remove_from_favorites,
    add_to_watchlist, remove_from_watchlist, load_favorites, load_watchlist
)
from pdfexport import create_movie_pdf
from api import get_person_filmography


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


def display_favorites_section() -> None:
    """Display user's favorite movies."""
    st.subheader("❤️ My Favorites")
    
    favorites_ids = load_favorites()
    if not favorites_ids:
        st.info("No favorite movies yet. Add some to get started!")
        return
    
    st.write(f"You have **{len(favorites_ids)}** favorite movies")


def display_watchlist_section() -> None:
    """Display user's watchlist."""
    st.subheader("📋 My Watchlist")
    
    watchlist = load_watchlist()
    if not watchlist:
        st.info("Your watchlist is empty. Add movies to watch later!")
        return
    
    st.write(f"You have **{len(watchlist)}** movies in your watchlist")
    
    cols = st.columns(5)
    for idx, movie in enumerate(watchlist):
        with cols[idx % 5]:
            st.write(f"**{movie.get('title', 'Unknown')[:15]}...**")
            if movie.get("poster_path"):
                st.image(f"{IMAGE_BASE_URL}{movie.get('poster_path')}")
            st.caption(f"⭐ {movie.get('vote_average', 'N/A')}")

def display_actor_filmography(person_id: int, actor_name: str) -> None:
    """Display filmography for an actor/director.
    
    Args:
        person_id: TMDB person ID
        actor_name: Name of the actor/director
    """
    st.subheader(f"🎬 Filmography of {actor_name}")
    
    filmography = get_person_filmography(person_id)
    
    if not filmography:
        st.info(f"No filmography information available for {actor_name}")
        return
    
    # Filter out movies without titles or release dates
    valid_films = [f for f in filmography if f.get('title') and f.get('release_date')]
    
    st.write(f"**{actor_name}** has appeared in **{len(valid_films)}** movies")
    
    # Display in a scrollable grid
    cols = st.columns(5)
    for idx, film in enumerate(valid_films[:20]):  # Show top 20 films
        with cols[idx % 5]:
            st.write(f"**{film.get('title', 'Unknown')[:12]}...**")
            if film.get("poster_path"):
                st.image(f"{IMAGE_BASE_URL}{film.get('poster_path')}")
            st.caption(f"{film.get('release_date', 'N/A')[:4]}")


def display_movie_comparison(movies: List[Dict]) -> None:
    """Display side-by-side comparison of movies.
    
    Args:
        movies: List of movie dictionaries (2-3 movies)
    """
    if len(movies) < 2:
        st.warning("Select at least 2 movies to compare")
        return
    
    st.subheader("⚖️ Movie Comparison")
    
    # Create columns for each movie
    cols = st.columns(len(movies))
    
    for col_idx, (col, movie) in enumerate(zip(cols, movies)):
        with col:
            st.write(f"### {movie.get('title', 'Unknown')}")
            
            if movie.get('poster_path'):
                st.image(f"{IMAGE_BASE_URL}{movie.get('poster_path')}")
            
            # Comparison data
            st.write("**Release Date:** " + str(movie.get('release_date', 'N/A')))
            st.write("**Rating:** " + f"{movie.get('vote_average', 'N/A')}/10")
            st.write("**Runtime:** " + f"{movie.get('runtime', 'N/A')} min")
            
            # Genres
            genres = movie.get('genres', [])
            if genres:
                genre_str = ", ".join([g['name'] for g in genres])
                st.write("**Genres:** " + genre_str)
            
            # Budget & Revenue
            if movie.get('budget') and movie.get('budget') > 0:
                st.write("**Budget:** " + f"${movie.get('budget'):,.0f}")
            
            if movie.get('revenue') and movie.get('revenue') > 0:
                st.write("**Revenue:** " + f"${movie.get('revenue'):,.0f}")
            
            st.write("**Popularity:** " + str(movie.get('popularity', 'N/A')))
    
    # Comparison table
    st.subheader("📊 Detailed Comparison")
    comparison_data = []
    
    comparison_data.append(['Metric'] + [m.get('title', 'Unknown')[:20] for m in movies])
    comparison_data.append(['Release Date'] + [m.get('release_date', 'N/A') for m in movies])
    comparison_data.append(['Rating'] + [f"{m.get('vote_average', 'N/A')}" for m in movies])
    comparison_data.append(['Runtime (min)'] + [str(m.get('runtime', 'N/A')) for m in movies])
    comparison_data.append(['Budget'] + [f"${m.get('budget', 0):,.0f}" if m.get('budget', 0) > 0 else 'N/A' for m in movies])
    comparison_data.append(['Revenue'] + [f"${m.get('revenue', 0):,.0f}" if m.get('revenue', 0) > 0 else 'N/A' for m in movies])
    comparison_data.append(['Popularity'] + [f"{m.get('popularity', 'N/A')}" for m in movies])
    comparison_data.append(['Vote Count'] + [str(m.get('vote_count', 'N/A')) for m in movies])
    
    # Convert to markdown table format for display
    table_str = ""
    for row in comparison_data:
        table_str += "| " + " | ".join(str(c) for c in row) + " |\n"
        if row == comparison_data[0]:
            table_str += "|" + " --- |" * len(row) + "\n"
    
    st.markdown(table_str)

def display_movie_action_buttons(movie: Dict) -> None:
    """Display favorite and watchlist action buttons.
    
    Args:
        movie: Movie dictionary
    """
    movie_id = movie.get('id')
    is_fav = is_favorited(movie_id)
    is_watch = is_in_watchlist(movie_id)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("❤️ " + ("Remove from Favorites" if is_fav else "Add to Favorites"), key=f"fav_{movie_id}", use_container_width=True):
            if is_fav:
                remove_from_favorites(movie_id)
                st.success("Removed from favorites!")
            else:
                add_to_favorites(movie_id)
                st.success("Added to favorites!")
            st.rerun()
    
    with col2:
        if st.button("📋 " + ("Remove from Watchlist" if is_watch else "Add to Watchlist"), key=f"watch_{movie_id}", use_container_width=True):
            if is_watch:
                remove_from_watchlist(movie_id)
                st.success("Removed from watchlist!")
            else:
                add_to_watchlist(movie)
                st.success("Added to watchlist!")
            st.rerun()
    
    with col3:
        pdf_bytes = create_movie_pdf(movie)
        st.download_button(
            label="📄 Download PDF",
            data=pdf_bytes,
            file_name=f"{movie.get('title', 'movie').replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

