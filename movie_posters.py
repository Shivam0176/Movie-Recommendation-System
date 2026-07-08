import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_posters_url(movie_name):
    api_key = os.getenv('omdb_apikey')
    url = 'https://www.omdbapi.com/'

    parameters = {
        't': movie_name,
        'apikey': api_key
    }

    response = requests.get(url,params=parameters)
    data = response.json()

    if data.get('Response') == "True":
        poster_url = data.get("Poster")

        if poster_url != 'N/A':
            return poster_url
        
        else:
            return 'No image availabel'
        
    else:
        return 'Movie not found in database'
    
