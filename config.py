"""Configuration and constants for Movie Detail App."""

import os
from typing import Optional

# TMDB API Configuration
API_KEY: Optional[str] = os.environ.get("TMDB_API_KEY")
BASE_URL: str = "https://api.themoviedb.org/3"
IMAGE_BASE_URL: str = "https://image.tmdb.org/t/p/w500"

# App Configuration
APP_TITLE: str = "Movie Detail App - TMDB"
CACHE_TTL: int = 3600  # Cache duration in seconds (1 hour)
