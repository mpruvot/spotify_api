from dotenv import load_dotenv
import os
import requests
import base64
from fastapi import FastAPI, Request, Cookie, Response
from fastapi.responses import HTMLResponse, RedirectResponse
import urllib.parse
import json
import datetime

app = FastAPI()

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = "http://localhost:8000/callback"

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1/"

@app.get("/", response_class=HTMLResponse)
def root():
    return "Welcome the Spotify App <a href='/login'>Login with Spotify</a>"

@app.get("/login")
def login():
    scope = "user-read-private user-read-email"
    
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': redirect_uri,
        'show_dialog': True
    }
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return RedirectResponse(auth_url)
    
@app.get("/callback")
def callback(request: Request, response: Response, error: str = None, code: str = None):
    if error:
        return {"error": error}
    
    if code:
        request_body = {
            'code': code,
            'grant_type': "authorization_code",
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret  # Correction ici
        }
        response = requests.post(TOKEN_URL, data=request_body)
        token_info = response.json()
        
        # Utilisation de cookies sécurisés pour stocker les tokens
        response.set_cookie(key="access_token", value=token_info['access_token'])
        response.set_cookie(key="refresh_token", value=token_info['refresh_token'])
        response.set_cookie(key="expires_in", value=str(datetime.datetime.now().timestamp() + token_info['expires_in']))
        
        return {"message": "Authentification réussie"}