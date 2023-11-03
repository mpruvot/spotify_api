from fastapi import FastAPI, HTTPException
from .oauth import get_token
from .manager import SpotifySearch
from requests import HTTPError
from .models import *


app = FastAPI()
token = get_token()
manager = SpotifySearch(token=token)

@app.get("/", response_description="Welcome message")
def home_root():
    """
    Root GET endpoint returning a welcome message.
    """
    return {"msg": "Hello World"}

@app.get("/artist/{name}", response_model=Artist, responses={404: {"description": "Artist not found"}})
def get_artist(name: str):
    """
    Retrieve an artist by name.
    """
    try:
        return manager.get_artist(name)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except HTTPError as he:
        raise HTTPException(status_code=400, detail=str(he))

@app.get("/album/{name}", response_model=Album, responses={404: {"description": "Album not found"}})
def get_album(name: str):
    """
    Retrieve an album by name.
    """
    try:
        return manager.get_album(name)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except HTTPError as he:
        raise HTTPException(status_code=400, detail=str(he))

@app.get("/track/{name}", response_model=Track, responses={404: {"description": "Track not found"}})
def get_track(name: str):
    """
    Retrieve a track by name.
    """
    try:
        return manager.get_track(name)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except HTTPError as he:
        raise HTTPException(status_code=400, detail=str(he))

@app.get("/playlist/{name}", response_model=Playlist, responses={404: {"description": "Playlist not found"}})
def get_playlist(name: str):
    """
    Retrieve a playlist by name.
    """
    try:
        return manager.get_playlist(name)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except HTTPError as he:
        raise HTTPException(status_code=400, detail=str(he))


