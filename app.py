import streamlit as st
import pickle
import pandas as pd
import requests 

api_key = "957495194da06c0106d4e9293bcd1c07"


#fetch poster
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=957495194da06c0106d4e9293bcd1c07&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500"+data['poster_path']

#recommend movies
def recommend(movie):
    movie_indx = movies[movies['title']==movie].index[0]
    distances = similarity[movie_indx] # distance matrix
    movies_list = sorted(list(enumerate(distances)),reverse=True , key = lambda x: x[1])[1:6]

    recommended_movies =[]
    recommended_posters = []
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies , recommended_posters

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')
selected_movie = st.selectbox('Select a movie to get recommendations:', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(len(names)):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
