import pandas as pd
import bz2file as bz2
import pickle
import streamlit as st
import requests

# register for an account at https://developers.themoviedb.org/3/getting-started/introduction
# register for an API Key at https://www.themoviedb.org/settings/api/new?type=developer
api_key = "83be9919b7c48c0b43c38c2799aa73a5"

# create function to retrieve movie posters
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/" + str(movie_id) + "?api_key=" + api_key + "&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# load preprocessed movie data
movies = bz2.BZ2File('movies.pbz2', 'rb')
movies = pickle.load(movies)

# load similarity scores
similarity = bz2.BZ2File('similarity.pbz2', 'rb')
similarity = pickle.load(similarity)

# create function to recommend top 5 movies based on descending order of similarity
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []

    for i in movies_list:
        # retrieve movie posters
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movie_posters


# streamlit user interface
st.title("Movie Recommender")
#st.subheader("Type or select a movie from the dropdown list")

# 2-column layout
col1, col2 = st.columns(2)

with col1:
    selected_movie_name = st.selectbox(
        label = "Type or select a movie from the dropdown list",
        options = movies['title'].values,
        label_visibility = "collapsed"
    )

with col2:
    # show top 5 recommendations on button click
    if st.button('Show Top 5 Recommendations'):
        names, posters = recommend(selected_movie_name)

# generate recommendations only after first search is done
if 'names' in locals():
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["#1 " + names[0], "#2 " + names[1], "#3 " + names[2], "#4 " + names[3], "#5 " + names[4]])

    tab1.subheader(names[0])
    tab1.image(posters[0], width=300)

    tab2.subheader(names[1])
    tab2.image(posters[1], width=300)

    tab3.subheader(names[2])
    tab3.image(posters[2], width=300)    

    tab4.subheader(names[3])
    tab4.image(posters[3], width=300)    

    tab5.subheader(names[4])
    tab5.image(posters[4], width=300)
