#importing all required dependencies
import pandas as pd
import numpy as np
import ast
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

#Loading the dataset
movies = pd.read_csv('Dataset\\tmdb_5000_movies.csv')
credits = pd.read_csv('Dataset\\tmdb_5000_credits.csv')

movies = movies.merge(credits,on='title')
movies = movies[['movie_id','title','genres','keywords','overview','cast','crew']]
movies.dropna(inplace=True)
movies.duplicated().sum()


def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])

    return L

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)

def convert_cast(obj):
    L = []
    for i in ast.literal_eval(obj)[:3]:
        L.append(i['name'])
        

    return L

movies['cast'] = movies['cast'].apply(convert_cast)

def fetch_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L
movies['crew'] = movies['crew'].apply(fetch_director)

movies['overview'] = movies['overview'].apply(lambda x:x.split())
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(' ','') for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(' ','') for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(' ','') for i in x])
movies['genres'] = movies['genres'].apply(lambda x: [i.replace(' ','') for i in x])

movies['tags'] = movies['overview'] + movies['cast'] + movies['genres'] + movies['crew'] + movies['keywords']

new_df = movies[['movie_id','title','tags']]

new_df['tags'] = new_df['tags'].apply(lambda x:" ".join(x))

new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())

ps = PorterStemmer() 

#function to remove similar words (eg: love, loving, loved -> love)
def stem(text):
    y = []

    for i in text.split():
        y.append(ps.stem(i))

    return " ".join(y)

new_df['tags'] = new_df['tags'].apply(stem)

cv = CountVectorizer(max_features=5000,stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

#deriving cosine distances between vectors
similarity = cosine_similarity(vectors)

def recommend(movie):
    movie_index =new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    for i in movies_list:
        print(new_df.iloc[i[0]].title)

pickle.dump(new_df.to_dict(),open('binary_files//movie_dict.pkl','wb'))
pickle.dump(similarity,open('binary_files//similarity.pkl','wb'))