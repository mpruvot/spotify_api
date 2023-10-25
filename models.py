from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict
from auth import *
import json

class Artist(BaseModel):
    name: str
    genres : Optional[list[str]] = None
    id : str
    external_urls: Optional[Dict[str, HttpUrl]] = None
    albums : Optional[List[str]] = []
    
class Track(BaseModel):
    name: str = Field(..., description="track name")
    artist_name : str = Field(..., description="artist name")
    album_name : str = Field(..., description="album name")
    release_date : str
    total_tracks : int
    label: Optional[str]
    
class Album(BaseModel):
    id: str
    name: str
    artists: List[Artist]
    release_date: str
    total_tracks: int

class Playlist(BaseModel):
    playlist_name: str = Field(None, description="playlist name")
    playlist_url: HttpUrl = Field(..., description="complete url of the spotify playlist")
    track_list: list[Track] = Field(default_factory=list, description="list of tracks in the playlist")
    

if __name__ == "__main__":
    token = get_token()
    
    
    def get_album():
        with open("mock_return.json", "r") as f:
            data = json.load(f)
            album = Album(**data)
            print(album)

    get_album()