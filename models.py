from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Union
from auth import *
import json

class Owner(BaseModel):
    display_name : str
    id : str
    type: str
    external_urls: Dict[str,HttpUrl]
    
    
class Artist(BaseModel):
    id: str = Field(..., description="artist ID")
    name: str = Field(..., description="artist name")
    genres: Optional[list[str]] = None
    external_urls: Optional[Dict[str, HttpUrl]] = None


class Album(BaseModel):
    id: str
    name: str
    artists: List[Artist]
    release_date: str
    total_tracks: int


class Track(BaseModel):
    id: str
    name: str = Field(..., description="track name")
    artists: Optional[List[Artist]] = Field(..., description="artist name")
    external_urls: Optional[Dict[str, HttpUrl]] = None
    album: Album
    label: Optional[str] = None
    explicit: bool


class Playlist(BaseModel):
    id: str
    name: str = Field(None, description="playlist name")
    description: Optional[str] = None
    owner: Owner
    external_urls: Optional[Dict[str, HttpUrl]] = None
    tracks: Optional[Dict[str, Union[HttpUrl, int]]] = None


if __name__ == "__main__":
    token = get_token()

    def get_playlist():
        with open("mock_return.json", "r") as f:
            data = json.load(f)
            playlist_data = data['playlists']['items'][0]
            pl = Playlist(**playlist_data)
            print(pl)

    get_playlist()
