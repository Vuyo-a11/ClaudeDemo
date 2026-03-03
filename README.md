# Movie Detail Streamlit App

A clean, professional Streamlit application for searching movies and viewing detailed information using **The Movie Database (TMDB) API**.

## Features

- **Movie Search**: Search for movies by title with Year | Title display format
- **Movie Selection**: Select from search results using a dropdown
- **Detailed Information**: Display comprehensive movie data including:
  - Poster image
  - Release date, runtime, and status
  - Rating and popularity metrics
  - Overview/synopsis
  - Genres
  - Budget and revenue (financial data)
  - Original language
- **Error Handling**: Graceful error messages for API failures
- **Caching**: Smart caching to reduce API calls
- **Responsive UI**: Modern layout with columns and clear visual hierarchy

## Project Structure

```
.
├── main.py          # Main app entry point with UI logic
├── config.py        # Configuration and constants
├── api.py           # TMDB API client with caching and error handling
├── utils.py         # UI rendering utilities
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
