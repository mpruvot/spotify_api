from fastapi import FastAPI, HTTPException, Response, Request
from fastapi.responses import RedirectResponse, HTMLResponse
import requests
from dotenv import load_dotenv
import os
import random
import string
import json
from models import Playlist, Artist

load_dotenv()

"""
def get_random_string(len: int = 16):
    letters_and_digits = string.ascii_letters + string.digits
    random_str = "".join(random.choice(letters_and_digits) for i in range(len))
    return random_str
"""

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/callback"
REQUEST_TOKEN_URL = "https://accounts.spotify.com/api/token"
REQUEST_SPOTIFY_ME = "https://api.spotify.com/v1/me"

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def home_root():
    return """<html>
                <body>
                    <p><a href="http://localhost:8000/login">PLEASE LOGIN</a></p>
                </body>
              </html>"""


@app.get("/login")
def login(response: Response):
    # Request User Authorization
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "user-read-private user-read-email",
    }
    url = "https://accounts.spotify.com/authorize"
    r = requests.get(url, params=params)
    try:
        r.raise_for_status()
        return RedirectResponse(url=r.url)

    except HTTPException as e:
        return str(e)


@app.get("/callback")
def callback(response: Response, code: str):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",  # Cela dépend de l'API, mais c'est souvent nécessaire
    }
    token_response = requests.post(REQUEST_TOKEN_URL, data=data, headers=headers)
    try:
        token_response.raise_for_status()
        token_data = token_response.json()
        response.set_cookie("access_token", value=token_data["access_token"])
        return token_data
    except HTTPException as e:
        return str(e)


@app.get("/user_info")
def user_info(request: Request):
    access_token = request.cookies.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    if not access_token:
        return {"error": "Not authorized"}
    data = requests.get(REQUEST_SPOTIFY_ME, headers=headers)
    user_data = data.json()
    return user_data


@app.get("/artist/{artist_name}")
def get_artist(request: Request, artist_name: str):
    access_token = request.cookies.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    search_url = "https://api.spotify.com/v1/search"
    artist_url = "https://api.spotify.com/v1/artists/"
    params = {
        "q": artist_name,
        "type": "artist",
    }
    data = requests.get(search_url, headers=headers, params=params)

    from_data = data.json()

    id = from_data["artists"]["items"][0]["id"]


    artist_info = requests.get(artist_url + id, headers=headers)

    from_artist_info = artist_info.json()

    artist = Artist(**from_artist_info)

    return artist

   