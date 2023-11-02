from fastapi import FastAPI, HTTPException, Response, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from oauth import get_token
from manager import SpotifySearch
from requests import HTTPError


app = FastAPI()
token = get_token()
manager = SpotifySearch(token=token)


@app.get("/")
def home_root():
    return {
        'message' : 'hello'
    }

@app.get("/artist/{name}")
def get_artist(name: str):
    try:
        return manager.get_artist(name)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except HTTPError as he:
        raise HTTPException(status_code=400, detail=str(he))

@app.get("/album/{name}")
def get_album(name: str):
    try:
        return manager.get_album(name)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except HTTPError as he:
        raise HTTPException(status_code=400, detail=str(he))

@app.get("/track/{name}")
def get_track(name: str):
    try:
        return manager.get_track(name)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except HTTPError as he:
        raise HTTPException(status_code=400, detail=str(he))

@app.get("/playlist/{name}")
def get_playlist(name: str):
    try:
        return manager.get_playlist(name)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except HTTPError as he:
        raise HTTPException(status_code=400, detail=str(he))

