from dotenv import load_dotenv
import os
import requests
import base64

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    token_url = "https://accounts.spotify.com/api/token"
    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode()).decode()

    token_headers = {"Authorization": f"Basic {client_creds_b64}"}
    token_data = {"grant_type": "client_credentials"}

    r = requests.post(token_url, data=token_data, headers=token_headers)
    r.raise_for_status()
    
    token_info = r.json()
    token = token_info['access_token']
    return token
  