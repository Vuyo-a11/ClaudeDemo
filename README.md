# Movie Detail Streamlit App

A clean, professional Streamlit application for searching movies and viewing detailed information using **The Movie Database (TMDB) API**.

## Features

- **Movie Search & Selection**: Search by title and choose from results presented as `Year | Title`.
- **Detailed Movie Information**: View extensive details including:
  - Poster, release date, runtime, status, and original language
  - Rating, popularity, and vote count
  - Overview/synopsis and genres
  - Budget & revenue financial data
- **👥 Cast & Crew**: Browse top cast/crew members with photos and roles.
- **🎬 Trailers & Videos**: Watch embedded trailers, teasers, and clips.
- **📖 Reviews**: Read user reviews along with rating and date.
- **🎯 Recommendations**: See similar movies based on your current selection.
- **📁 Favorites & 📋 Watchlist**: Save movies locally and view/manage them from the sidebar.
- **👥 Movie Comparison**: Compare two or three titles side‑by‑side on key metrics.
- **🌟 Actor/Director Filmography**: Search for talent and explore their credits.
- **🎲 Surprise Me**: Get a random movie suggestion, optionally filtered by genre.
- **🎨 Theme Toggle**: Switch between light and dark color modes.
- **⭐ Personal Ratings**: Rate movies and track your rating history.
- **📊 Statistics Dashboard**: View charts summarizing your favorites, watchlist, budgets, etc.
- **PDF Export**: Download detailed movie info as a styled PDF.
- **🔥 Trending & Top-Rated**: Browse TMDB’s trending and all-time best films.
- **Error Handling & Caching**: Clear warnings for API issues and intelligent caching to minimize requests.
- **Responsive UI**: Clean, modern layout optimized for ease of use.

## Project Structure

```
.
├── main.py          # Main app entry point with UI logic
├── config.py        # Configuration and constants
├── api.py           # TMDB API client with caching and error handling
├── utils.py         # UI rendering utilities
├── storage.py       # Local persistence for favorites, watchlist, ratings
├── pdfexport.py     # PDF generation logic
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## Best Practices Implemented

✅ **Modular Architecture**: Separated concerns (API, Config, Utils, UI)  
✅ **Type Hints**: Full type annotations for better code quality  
✅ **Docstrings**: Clear documentation for all functions  
✅ **Error Handling**: Try-except blocks with user-friendly messages  
✅ **Caching**: Streamlit `@st.cache_data` for API efficiency  
✅ **Constants**: Centralized configuration in `config.py`  
✅ **Session State**: Proper state management across reruns  
✅ **Input Validation**: Validation of search queries and responses  

## Installation

1. Create a Python environment (venv or conda):
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # macOS/Linux
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your TMDB API key:
   ```powershell
   # Windows PowerShell
   $env:TMDB_API_KEY="your_key_here"
   
   # Windows CMD
   set TMDB_API_KEY=your_key_here
   
   # macOS/Linux
   export TMDB_API_KEY="your_key_here"
   ```

4. Run the app:
   ```bash
   streamlit run main.py
   ```

The app will open in your browser at `http://localhost:8501`

## Configuration

- **TMDB_API_KEY**: Required environment variable containing your TMDB API key
- **CACHE_TTL**: Cache duration in seconds (default: 3600 = 1 hour)
- Modify `config.py` to change constants or timeouts

## Notes

- API key is never hardcoded—always use environment variables
- Results are cached to minimize API calls and improve performance
- The app requires internet connection for TMDB API access

## Development Notes

For development and testing, commits trace feature progress:
- Initial setup & project structure
- Environment variable security
- Refactoring for best practices (modular, type hints, caching, error handling)
- Enhanced UI with better formatting

Enjoy exploring movies with this professional Streamlit app! 🎬
