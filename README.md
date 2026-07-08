# 🎬 Movie Recommendation System

A content-based movie recommendation system that suggests similar movies based on plot overview, genres, cast, crew, and keywords. Built using the TMDB 5000 Movie Dataset and deployed as an interactive web app with Streamlit.

## 🚀 Live Demo

Check out the live app here: [https://huggingface.co/spaces/Shivambhusari/movie-recommender](https://huggingface.co/spaces/Shivambhusari/movie-recommender)

## Overview

This project recommends movies similar to a user-selected title by analyzing the *content* of each movie rather than user ratings or behavior. It combines a movie's overview, genres, keywords, top cast, and director into a single "tags" feature, vectorizes the text, and computes similarity scores between movies using cosine similarity.

## Features

- Select any movie from a dropdown list and get 5 similar movie recommendations
- Fetches and displays movie posters for each recommendation using the OMDb API
- Fast recommendations powered by a precomputed similarity matrix
- Simple, interactive Streamlit web interface

## How It Works

The recommendation pipeline follows these steps:

1. **Data Collection** — Uses the TMDB 5000 Movies and Credits datasets, merged on movie title.
2. **Feature Selection** — Keeps only relevant columns: `movie_id`, `title`, `genres`, `keywords`, `overview`, `cast`, `crew`.
3. **Preprocessing**
   - Drops missing values
   - Parses stringified JSON columns (`genres`, `keywords`, `cast`, `crew`) using `ast.literal_eval`
   - Extracts genre and keyword names
   - Extracts the top 3 cast members
   - Extracts the director's name from the crew list
   - Removes spaces within names/words (e.g., `"Sam Worthington"` → `"SamWorthington"`) so multi-word names are treated as a single token
4. **Tag Creation** — Combines `overview`, `cast`, `genres`, `crew`, and `keywords` into a single `tags` column and converts it to lowercase text.
5. **Stemming** — Applies Porter Stemming (via NLTK) to reduce words to their root form (e.g., `loving`, `loved` → `love`).
6. **Vectorization** — Converts the `tags` text into numerical vectors using `CountVectorizer` (bag-of-words, top 5000 features, English stop words removed).
7. **Similarity Computation** — Calculates pairwise **cosine similarity** between all movie vectors to build a similarity matrix.
8. **Recommendation** — For a selected movie, sorts all other movies by similarity score and returns the top 5 closest matches.
9. **Serialization** — The processed movie data and similarity matrix are saved as `.pkl` files for fast loading in the app.

## Tech Stack

- **Python 3**
- **Pandas / NumPy** — data manipulation
- **NLTK** — text stemming
- **scikit-learn** — `CountVectorizer` and `cosine_similarity`
- **Streamlit** — web app interface
- **OMDb API** — fetching movie posters
- **Pickle** — model/data serialization

## Project Structure

```
movie-recommender-system/
│
├── movie-recommender-system.ipynb   # Data preprocessing, feature engineering & model building
├── app.py                            # Streamlit app
├── movie_posters.py                  # OMDb API integration for fetching posters
├── .env                               # Stores OMDb API key (not committed)
│
├── Dataset/
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
│
└── binary_files/
    ├── movie_dict.pkl                # Serialized processed movie data
    └── similarity.pkl                # Serialized cosine similarity matrix
```

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Shivam0176/Movie-Recommendation-System.git
cd movie-recommender-system
```

### 2. Install dependencies

```bash
pip install pandas numpy nltk scikit-learn streamlit requests python-dotenv
```

### 3. Download the dataset

Download the [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) from Kaggle and place the following files inside a `Dataset/` folder:
- `tmdb_5000_movies.csv`
- `tmdb_5000_credits.csv`

### 4. Get an OMDb API key

Sign up for a free API key at [omdbapi.com](https://www.omdbapi.com/apikey.aspx), then create a `.env` file in the project root:

```
omdb_apikey=your_api_key_here
```

### 5. Generate the model files

Run the python file `recommendation-system.py` to preprocess the data and generate `movie_dict.pkl` and `similarity.pkl`. these files will be in a `binary_files/` folder in the project root.

### 6. Run the app

```bash
streamlit run app.py
```

The app will open in your browser, typically at `http://localhost:8501`.

## Usage

1. Select a movie from the dropdown list.
2. Click the **Recommend** button.
3. View the top 5 recommended movies along with their posters.

## Future Improvements

- Use TF-IDF or word embeddings (e.g., Word2Vec, BERT) instead of `CountVectorizer` for richer semantic similarity
- Add caching/error handling for OMDb API failures and rate limits
- Deploy the app publicly (e.g., Streamlit Community Cloud)
- Add filters for genre, release year, or rating
- Make file paths OS-independent (currently uses Windows-style paths)



## License

This project is open source and available under the [MIT License](LICENSE).
