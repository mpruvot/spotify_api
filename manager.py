import requests
from requests import HTTPError
from models import Playlist, Track, Album, Artist
from oauth import get_token


class SpotifySearch():
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
        try:
            r.raise_for_status()
            response = r.json()
            return response[f"{genre}s"]["items"][0]["id"]

        except HTTPError as err:
            return str(err)

    def get_artist(self, name: str) -> Artist:
        artist_id = self.get_id(name=name, genre="artist")

        if not artist_id:
            raise ValueError(f"No artist found for {name}")
        artist_info = requests.get(
            url=self.ARTIST_URL + artist_id, headers=self.HEADERS
        )
        try:
            artist_info.raise_for_status()
            artist_data = artist_info.json()
            artist = Artist(**artist_data)
            return artist
        except HTTPError as err:
            raise HTTPError(
                f"HTTP error occurred: {str(err)} - {artist_info.text}"
            ) from err

    def get_track(self, name: str) -> Track:
        track_id = self.get_id(name=name, genre="track")

        if not track_id:
            raise ValueError(f"No track found for {name}")
        track_info = requests.get(
            url=self.TRACK_URL + track_id, headers=self.HEADERS
        )
        try:
            track_info.raise_for_status()
            track_data = track_info.json()
            track = Track(**track_data)
            return track
        except HTTPError as err:
            raise HTTPError(
                f"HTTP error occurred: {str(err)} - {track_info.text}"
            ) from err
            
    def get_album(self, name: str) -> Album:
        album_id = self.get_id(name=name, genre="album")

        if not album_id:
            raise ValueError(f"No album found for {name}")
        album_info = requests.get(
            url=self.ALBUM_URL + album_id, headers=self.HEADERS
        )
        try:
            album_info.raise_for_status()
            album_data = album_info.json()
            album = Album(**album_data)
            return album
        except HTTPError as err:
            raise HTTPError(
                f"HTTP error occurred: {str(err)} - {album_info.text}"
            ) from err

    def get_playlist(self, name: str) -> Playlist:
        playlist_id = self.get_id(name=name, genre="playlist")

        if not playlist_id:
            raise ValueError(f"No playlist found for {name}")
        playlist_info = requests.get(
            url=self.PLAYLIST_URL + playlist_id, headers=self.HEADERS
        )
        try:
            playlist_info.raise_for_status()
            playlist_data = playlist_info.json()
            playlist = Playlist(**playlist_data)
            return playlist
        except HTTPError as err:
            raise HTTPError(
                f"HTTP error occurred: {str(err)} - {playlist_info.text}"
            ) from err
