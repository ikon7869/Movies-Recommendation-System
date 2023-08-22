import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    res = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=be099fad8c28da47ef10db9623f3b1c7'.format(movie_id))
    data = res.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie):
    movie_index = movies_data[movies_data['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        recommended_movies.append(movies_data.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movies_data.iloc[i[0]].movie_id))
    return recommended_movies,recommended_movies_posters

movies = pickle.load(open('movies.pkl','rb'))
movies_data = pd.DataFrame(movies)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title("Movies Recommendation System")
selected_movie_name = st.selectbox('',movies_data['title'].values)

if st.button('Recommend'):
    names,posters= recommend(selected_movie_name)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

    