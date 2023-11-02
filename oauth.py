from dotenv import load_dotenv
import os
import requests
from requests import HTTPError
import base64


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = "http://localhost:8000/callback"

client_creds = f"{client_id}:{client_secret}"
client_creds_b64 = base64.b64encode(client_creds.encode())

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1/"

DATA = {
    "grant_type" : "client_credentials"
}

HEADERS = {
    "Authorization" : f"Basic {client_creds_b64.decode()}",
    "Content-Type" : "application/x-www-form-urlencoded"
}

def get_token():
    r = requests.post(TOKEN_URL, headers=HEADERS, data=DATA)
    try:
        r.raise_for_status()
        response = r.json()
        return response['access_token']
    except HTTPError as err:
        raise err

