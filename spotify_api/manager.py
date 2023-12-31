import requests
from requests import HTTPError
from .models import Playlist, Track, Album, Artist
from .oauth import get_token
import json


class SpotifySearch:
    """
    Handles search operations against the Spotify API.
    """

    def __init__(self, token: str) -> None:
        self.token = token
        self.HEADERS = {"Authorization": f"Bearer {self.token}"}

    ALLOWED_GENRES = ["artist", "playlist", "album", "track"]

    SEARCH_URL = "https://api.spotify.com/v1/search"
    ARTIST_URL = "https://api.spotify.com/v1/artists/"
    ALBUM_URL = "https://api.spotify.com/v1/albums/"
    TRACK_URL = "https://api.spotify.com/v1/tracks/"
    PLAYLIST_URL = "https://api.spotify.com/v1/playlists/"

    def get_id(self, name: str, genre: str, limit: int = 1, offset: int = 0):
        """
        Get Spotify ID for a name and genre.
        """
        if genre.lower() not in self.ALLOWED_GENRES:
            raise ValueError(
                "Wrong input, genre should be <artist> / <playlist> / <album> / <track>"
            )
        params = {
            "q": name.lower(),
            "type": genre.lower(),
            "limit": limit,
            "offset": offset,
        }

        r = requests.get(url=self.SEARCH_URL, headers=self.HEADERS, params=params)
        r.raise_for_status()
        response = r.json()
        genre_items = response.get(f"{genre}s", {}).get("items")
        if genre_items:
            return genre_items[0].get("id")
        else:
            raise ValueError(f"{genre.capitalize()} not found")

    def get_artist(self, name: str) -> Artist:
        """
        Retrieve artist by name.
        """
        artist_id = self.get_id(name=name, genre="artist")
        if not artist_id:
            raise ValueError(f"No artist found for {name}")

        artist_info = requests.get(
            url=f"{self.ARTIST_URL}{artist_id}", headers=self.HEADERS
        )
        artist_info.raise_for_status()
        artist_data = artist_info.json()
        artist = Artist(**artist_data)
        return artist

    def get_track(self, name: str) -> Track:
        """
        Retrieve track by name.
        """
        track_id = self.get_id(name=name, genre="track")

        if not track_id:
            raise ValueError(f"No track found for {name}")
        track_info = requests.get(url=self.TRACK_URL + track_id, headers=self.HEADERS)
        track_info.raise_for_status()
        track_data = track_info.json()
        track = Track(**track_data)
        return track

    def get_album(self, name: str) -> Album:
        """
        Retrieve album by name.
        """
        album_id = self.get_id(name=name, genre="album")

        if not album_id:
            raise ValueError(f"No album found for {name}")
        album_info = requests.get(url=self.ALBUM_URL + album_id, headers=self.HEADERS)
        album_info.raise_for_status()
        album_data = album_info.json()
        album = Album(**album_data)
        return album

    def get_playlist(self, name: str) -> Playlist:
        """
        Retrieve playlist by name.
        """
        playlist_id = self.get_id(name=name, genre="playlist")

        if not playlist_id:
            raise ValueError(f"No playlist found for {name}")
        playlist_info = requests.get(
            url=self.PLAYLIST_URL + playlist_id, headers=self.HEADERS
        )
        playlist_info.raise_for_status()
        playlist_data = playlist_info.json()
        playlist = Playlist(**playlist_data)
        return playlist
