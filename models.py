from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

class Artist(BaseModel):
    name: str

class Track(BaseModel):
    track_name: str = Field(..., description="track name")
    artist_name: str = Field(..., description="artist name")
    album_name: str = Field(..., description="album name")

class Playlist(BaseModel):
    playlist_name: str = Field(None, description="playlist name")
    playlist_url: HttpUrl = Field(..., description="complete url of the spotify playlist")
    track_list: list[Track] = Field(default_factory=list, description="list of tracks in the playlist")
    
class Album(BaseModel):
    name : str = Field(..., description="name of the album")
    artists: List[Artist]
    release_date : str = Field(..., description="release_date")
    track_list: Optional[list[Track]] = Field(default_factory=list, description="list of tracks in the album") 