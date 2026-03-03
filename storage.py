"""Persistent storage management for favorites and watchlist."""

import json
import os
from typing import List, Dict, Set
from pathlib import Path


STORAGE_DIR = Path.home() / ".movie_app"
FAVORITES_FILE = STORAGE_DIR / "favorites.json"
WATCHLIST_FILE = STORAGE_DIR / "watchlist.json"


def ensure_storage_dir() -> None:
    """Create storage directory if it doesn't exist."""
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)


def load_favorites() -> Set[int]:
    """Load favorites from disk.
    
    Returns:
        Set of movie IDs in favorites
    """
    ensure_storage_dir()
    if FAVORITES_FILE.exists():
        try:
            with open(FAVORITES_FILE, 'r') as f:
                return set(json.load(f))
        except (json.JSONDecodeError, IOError):
            return set()
    return set()


def save_favorites(favorites: Set[int]) -> None:
    """Save favorites to disk.
    
    Args:
        favorites: Set of movie IDs
    """
    ensure_storage_dir()
    with open(FAVORITES_FILE, 'w') as f:
        json.dump(list(favorites), f)


def load_watchlist() -> List[Dict]:
    """Load watchlist from disk.
    
    Returns:
        List of movie dictionaries in watchlist
    """
    ensure_storage_dir()
    if WATCHLIST_FILE.exists():
        try:
            with open(WATCHLIST_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_watchlist(watchlist: List[Dict]) -> None:
    """Save watchlist to disk.
    
    Args:
        watchlist: List of movie dictionaries
    """
    ensure_storage_dir()
    with open(WATCHLIST_FILE, 'w') as f:
        json.dump(watchlist, f, indent=2)


def add_to_favorites(movie_id: int) -> None:
    """Add movie to favorites.
    
    Args:
        movie_id: TMDB movie ID
    """
    favorites = load_favorites()
    favorites.add(movie_id)
    save_favorites(favorites)


def remove_from_favorites(movie_id: int) -> None:
    """Remove movie from favorites.
    
    Args:
        movie_id: TMDB movie ID
    """
    favorites = load_favorites()
    favorites.discard(movie_id)
    save_favorites(favorites)


def is_favorited(movie_id: int) -> bool:
    """Check if movie is in favorites.
    
    Args:
        movie_id: TMDB movie ID
        
    Returns:
        True if movie is favorited, False otherwise
    """
    return movie_id in load_favorites()


def add_to_watchlist(movie: Dict) -> None:
    """Add movie to watchlist.
    
    Args:
        movie: Movie dictionary to add
    """
    watchlist = load_watchlist()
    # Avoid duplicates
    if not any(m.get('id') == movie.get('id') for m in watchlist):
        watchlist.append(movie)
        save_watchlist(watchlist)


def remove_from_watchlist(movie_id: int) -> None:
    """Remove movie from watchlist.
    
    Args:
        movie_id: TMDB movie ID
    """
    watchlist = load_watchlist()
    watchlist = [m for m in watchlist if m.get('id') != movie_id]
    save_watchlist(watchlist)


def is_in_watchlist(movie_id: int) -> bool:
    """Check if movie is in watchlist.
    
    Args:
        movie_id: TMDB movie ID
        
    Returns:
        True if movie is in watchlist, False otherwise
    """
    watchlist = load_watchlist()
    return any(m.get('id') == movie_id for m in watchlist)


# --- personal ratings storage ---
RATINGS_FILE = STORAGE_DIR / "ratings.json"

def load_ratings() -> Dict[int, float]:
    """Load personal ratings from disk. Returns mapping movie_id->rating"""
    ensure_storage_dir()
    if RATINGS_FILE.exists():
        try:
            with open(RATINGS_FILE, 'r') as f:
                return {int(k): float(v) for k,v in json.load(f).items()}
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_ratings(ratings: Dict[int, float]) -> None:
    """Save ratings dictionary to disk"""
    ensure_storage_dir()
    with open(RATINGS_FILE, 'w') as f:
        json.dump({str(k): v for k,v in ratings.items()}, f)


def set_rating(movie_id: int, rating: float) -> None:
    """Add or update personal rating for a movie"""
    ratings = load_ratings()
    ratings[movie_id] = rating
    save_ratings(ratings)


def get_rating(movie_id: int) -> Optional[float]:
    """Retrieve personal rating for given movie"""
    return load_ratings().get(movie_id)


def remove_rating(movie_id: int) -> None:
    """Delete personal rating for a movie"""
    ratings = load_ratings()
    if movie_id in ratings:
        del ratings[movie_id]
        save_ratings(ratings)
