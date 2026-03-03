# Movie Detail Streamlit App

This is a simple Streamlit application that allows users to search for movies and view detailed information using The Movie Database (TMDB) API.

## Features

1. **Search Movies**: Users can enter a query to search for movies. Results show as `Year | Title`.
2. **Select a Movie**: After searching, users can select a movie from a dropdown.
3. **View Details**: Displays title, poster, release date, overview, genres, runtime, rating, popularity, status, language, budget, revenue, and raw JSON response.

## Implementation Plan

- **Initial Setup**: Create Streamlit project with requirements
- **Search Page**: Implement search input and API call to `/search/movie`.
- **Selection & Details**: Show dropdown of search results. Fetch details from `/movie/{id}`.
- **Display Info**: Render all valuable fields from API response, including raw JSON.
- **Polish & Commit**: Add comments, README, and commit history traces.

## Run the App

1. Create a Python environment (venv or conda).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch Streamlit:
   ```bash
   streamlit run main.py
   ```

## Notes

- TMDB API key should be provided via the `TMDB_API_KEY` environment variable. Set it before launching the app, e.g. `set TMDB_API_KEY=YOUR_KEY` on Windows or `export TMDB_API_KEY=YOUR_KEY` on macOS/Linux.
- Commits should trace feature development and incremental progress.

Enjoy exploring movies! 🐼
