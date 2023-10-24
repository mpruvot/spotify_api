from fastapi import FastAPI, HTTPException
from auth import get_token
from manager import *


app = FastAPI()
manager = PlaylistManager()

@app.get("/")
def home_root():
    return {"message": "home_page"}

#Token Tester
@app.get("/callback")
def test():
    token = get_token()
    return token

@app.get("/playlist/{playlist_name}")
def get_playlist(playlist_name : str, offset: int = 0, limit: int = 1):
    try:
       return manager.get_public_playlist(playlist_name, offset, limit)
    except requests.exceptions.HTTPError as err:
        raise HTTPException(status_code=404, detail=str(f"{err}"))

