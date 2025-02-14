
from dotenv import load_dotenv
import os
import requests
import datetime as dt

def configure():
    load_dotenv()

def rawg_api():
    configure()
    api_key =  os.getenv("API_KEY")
    base_url = "https://api.rawg.io/api"
    return api_key, base_url

def get_game_data(api_key, base_url):
    week_ago = dt.datetime.now() - dt.timedelta(days=7)
    response = requests.get(f"{base_url}/games?key={api_key}&dates={week_ago.strftime('%Y-%m-%d')},{dt.datetime.now().strftime('%Y-%m-%d')}&ordering=-added")
    #response = requests.get(f"{base_url}/games?key={api_key}")

    games_data=[]
    for game in response.json()["results"]:
        games_data.append({
            "name": game["name"],
            "released": game["released"],
            "genres": game["genres"],
            #"description": game["description"]
        })
        
    return games_data

def main():
    api_key, base_url = rawg_api()
    print(get_game_data(api_key, base_url))
    

if __name__ == "__main__":
    main()
    