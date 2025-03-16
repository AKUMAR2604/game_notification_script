
from dotenv import load_dotenv
import os
import requests
import datetime as dt
from smtplib import SMTP
from email.mime.text import MIMEText
import ssl
import regex as re

#loading env variables
def configure():
    load_dotenv()

def rawg_api():
    configure()
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    base_url = "https://api.rawg.io/api"
    return api_key, base_url

def get_game_data(api_key, base_url)->list:
    week_ago = dt.datetime.now() - dt.timedelta(days=7)
    try:
        response = requests.get(f"{base_url}/games?key={api_key}&dates={week_ago.strftime('%Y-%m-%d')},{dt.datetime.now().strftime('%Y-%m-%d')}&ordering=-added")
    except requests.exceptions.HTTPError as e:
        return f"error:{e}"
    


    games_data=[]
    for game in response.json()["results"]:
        games_data.append({
            "name": game["name"],
            "released": game["released"],
            "genres": game["genres"],
            "id": game["id"],
        })

        for game in games_data:
            game_id = game["id"]
            desc_response = requests.get(f"{base_url}/games/{game_id}?key={api_key}")
            desc_response.raise_for_status()
            game["description"] = desc_response.json().get("description")
        



    return games_data


    

def automate_email(games_data:list)->None:

    #defining email variables

    smtp_server= 'smtp.gmail.com'
    port= 587
    email=  os.getenv("EMAIL")
    if not email:
        raise ValueError("EMAIL environment variable is not set")
    password=  os.getenv("PASSWORD")
    if not password:
        raise ValueError("PASSWORD environment variable is not set")
    smtp_username= email
    smtp_password=password
    sender=email
    receiver=email

    #creating email object with MIMEtext
    body = "Here are the games released in the last week:\n\n"
    for game in games_data:
        body += f"Name: {game['name']}\n\n"
        body += f"Released: {game['released']}\n\n"
        body += f"Genres: {', '.join([genre['name'] for genre in game['genres']])}\n\n"
        body += f"Description: {game.get('description', 'No description available')}\n\n"
        body += "\n"
        #removing html tags
        body = re.sub('<[^<]+?>', '', body)
    

    msg = MIMEText(body)
    msg['Subject']="games released this week"
    msg["From"]=sender
    msg["To"]=receiver

    #sending email
    try:
        context = ssl.create_default_context()
        with SMTP(smtp_server, port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender, receiver, msg.as_string())
            server.quit()
            print("email sent")
    except Exception as e:
        print(f"error:{e}")

        
def main():
    api_key, base_url = rawg_api()
    games = get_game_data(api_key, base_url)
    automate_email(games)

    
if __name__ == "__main__":
    main()


    