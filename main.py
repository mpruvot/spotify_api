from fastapi import FastAPI
import requests
import json
from auth import get_token

app = FastAPI()


@app.get("/")
def home_root():
    return {"message": "home_page"}


@app.get("/callback")
def test():
    token = get_token()
    return token
