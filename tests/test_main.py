import pytest
import json
from fastapi.testclient import TestClient
from spotify_api.main import app

from spotify_api.models import *

#Create a TestClient instance for testing
client = TestClient(app)


def test_home_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
    
def test_get_artist():
    response = client.get("/artist/radiohead")
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'Radiohead'
    assert data['id'] == '4Z8W4fKeB5YxbusRsdQVPb'

def test_get_artist_not_found():
    response = client.get("/artist/iuoqshgilqgkhksqghoiesfht")
    assert response.status_code == 404
    assert response.json() == {"detail": "Artist not found"}

def test_get_album():
    response = client.get("/album/Ok%Computer")
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'OK Computer'  
    assert data['id'] == '6dVIqQ8qmQ5GBnJ9shOYGE'

def test_get_album_not_found():
    response = client.get("/album/gqdsjfhjghksjfgjfgjd")
    assert response.status_code == 404
    assert response.json() == {"detail": "Album not found"}

def test_get_track_creep():
    response = client.get("/track/Creep")
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'Creep'
    assert data['id'] == '70LcF31zb1H0PyJoS1Sx1r'

def test_get_track_not_found():
    response = client.get("/track/qsdklfjmqskldfjmslkdfj")
    assert response.status_code == 404
    assert response.json() == {"detail": "Track not found"}

def test_get_playlist_radiohead_essentials():
    response = client.get("/playlist/Radiohead%Essentials")
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'RADIOHEAD ESSENTIALS'
    assert data['id'] == '5QZqx7YKM6Ktiltl8At1Uy'

def test_get_playlist_not_found():
    response = client.get("/playlist/qmslkdfjmqslkdjfmqlskdjf")
    assert response.status_code == 404
    assert response.json() == {"detail": "Playlist not found"}
