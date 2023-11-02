from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Union

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


class PlaylistTracksItem(BaseModel):
    added_at: str
    track: Track

class PlaylistTracks(BaseModel):
    href: str
    items: List[PlaylistTracksItem]

class Playlist(BaseModel):
    id: str
    name: str = Field(None, description="playlist name")
    description: Optional[str] = None
    owner: Owner
    external_urls: Optional[Dict[str, HttpUrl]] = None
    tracks: PlaylistTracks

