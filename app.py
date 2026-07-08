import streamlit as st
import pickle
import pandas as pd
from movie_posters import fetch_posters_url

@st.cache_resource
def load_data():
    print("Loading movie dictionary...")
    movies_dict = pickle.load(open('binary_files\\movie_dict.pkl','rb'))
    movies_df = pd.DataFrame(movies_dict)
    
    print("Loading similarity matrix...")
    similarity_matrix = pickle.load(open('binary_files\\similarity.pkl','rb'))
    
    print("Data loaded successfully!")
    return movies_df, similarity_matrix

movies, similarity = load_data()

st.title('Movie Recommendation System')

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    recommended_movies = []
    for i in movies_list:
        
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

def diplay_posters(movies_list):
    title_cols = st.columns(len(movies_list))
    # Row 1 (Titles)
    for index, col in enumerate(title_cols):
        with col:
            st.write(f'**{movies_list[index]}**')
            
    # Row 2 (Posters)
    poster_cols = st.columns(len(movies_list))
    for index, col in enumerate(poster_cols):
        with col:
            poster = fetch_posters_url(movies_list[index])
            if poster:
                st.image(poster, use_container_width=True)
            else:
                st.text("No Poster Available")

selected_movie_name = st.selectbox(
    'Movies List',
    movies['title'].values
)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    diplay_posters(recommendations)