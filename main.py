import streamlit as st
import requests
import os

API_KEY = os.environ.get("TMDB_API_KEY")
if not API_KEY:
    st.error("TMDB_API_KEY environment variable not set. Please export your API key before running.")
    st.stop()

BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

st.title("Movie Detail App - TMDB")

# search section
query = st.text_input("Search for a movie")
if st.button("Search") and query:
    params = {"api_key": API_KEY, "query": query}
    res = requests.get(f"{BASE_URL}/search/movie", params=params)
    data = res.json()
    results = data.get("results", [])
    if results:
        # show selection
        options = {f"{r.get('release_date','')[:4]} | {r.get('title')}": r.get('id') for r in results}
        choice = st.selectbox("Select a movie", list(options.keys()))
        if choice:
            movie_id = options[choice]
            detail_res = requests.get(f"{BASE_URL}/movie/{movie_id}", params={"api_key": API_KEY})
            detail = detail_res.json()
            # display details
            st.header(detail.get("title"))
            if detail.get("poster_path"):
                st.image(f"{IMAGE_BASE}{detail.get('poster_path')}")
            st.write("**Release Date:**", detail.get("release_date"))
            st.write("**Overview:**", detail.get("overview"))
            st.write("**Genres:**", ", ".join([g['name'] for g in detail.get('genres', [])]))
            st.write("**Runtime:**", detail.get("runtime"), "minutes")
            st.write("**Rating:**", detail.get("vote_average"), "/ 10")
            st.write("**Popularity:**", detail.get("popularity"))
            st.write("**Status:**", detail.get("status"))
            st.write("**Original Language:**", detail.get("original_language"))
            st.write("**Budget:**", detail.get("budget"))
            st.write("**Revenue:**", detail.get("revenue"))
    else:
        st.warning("No results found")
