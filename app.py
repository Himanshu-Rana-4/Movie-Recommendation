import streamlit as st
import pickle 
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path



def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0] # Take index of the given movie
    dist = similarity[movie_index]
    movies_list = sorted(list(enumerate(dist)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        # Fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

# Centered title using HTML and CSS
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
    }
    .movie-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 200px;
    }
    .movie-title {
        height: 50px; /* Adjust as needed */
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        font-size: 16px;
        margin-bottom: 10px;
    }
    .movie-poster {
        max-height: 150px;
    }
    </style>
    <div class="title">Movie Recommendation System</div>
    """,
    unsafe_allow_html=True
)

select_movie_name = st.selectbox(
    'Select a movie:',
    (movies['title'].values)
)

if st.button('Recommend'):
    names, posters = recommend(select_movie_name)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"<div class='movie-card'><div class='movie-title'>{names[0]}</div><img class='movie-poster' src='{posters[0]}'></div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"<div class='movie-card'><div class='movie-title'>{names[1]}</div><img class='movie-poster' src='{posters[1]}'></div>", unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"<div class='movie-card'><div class='movie-title'>{names[2]}</div><img class='movie-poster' src='{posters[2]}'></div>", unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"<div class='movie-card'><div class='movie-title'>{names[3]}</div><img class='movie-poster' src='{posters[3]}'></div>", unsafe_allow_html=True)
        
    with col5:
        st.markdown(f"<div class='movie-card'><div class='movie-title'>{names[4]}</div><img class='movie-poster' src='{posters[4]}'></div>", unsafe_allow_html=True)
