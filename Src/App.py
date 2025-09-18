import streamlit as st
import pickle
import pandas as pd
import requests



movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies_recv = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=db209508643c0755bc9e51b2e4803945&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recomend(movie):
    movie_index = movies_recv[movies_recv['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key = lambda x : x[1])[:6]
    
    recomended_movies = []
    recomended_movies_poster = []
    for i in movies_list:
        movie_id = movies_recv.iloc[i[0]].movie_id
        recomended_movies.append(movies_recv.iloc[i[0]].title)
        # recomended_movies_poster.append(fetch_poster(movie_id))
    return recomended_movies, recomended_movies_poster


st.title("Movie Recomender System")
selected_movie = st.selectbox(" ", movies_recv['title'].values)



if st.button('Recomend'):
    names, posters = recomend(selected_movie)
    
    for i in names:
        st.write(i)
    