import json
from fastapi import HTTPException
import requests
from models import Playlist, Track, Album
from auth import get_token
from pydantic import TypeAdapter
from typing import List


class PlaylistManager:
    def __init__(self) -> None:
        self.playlists = []
        self.token = get_token()

    def get_public_playlist(
        self, playlist_name: str, offset: int = 0, limit: int = 1
    ) -> list[Playlist]:
        if offset < 0 or limit < 1:
            raise HTTPException(
                status_code=400,
                detail="Invalid pagination parameters: offset and limit must be positive.",
            )
        url = f"https://api.spotify.com/v1/search"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {
            "q": playlist_name,
            "type": "playlist",
            "limit": limit,
            "offset": offset,
        }
        response = requests.get(url, headers=headers, params=params)
        try:
            response.raise_for_status()
            search_results = response.json()

            if search_results["playlists"]["total"] > 0:
                playlists_found = search_results["playlists"]["items"]

                if offset < len(playlists_found):
                    playlist_info = playlists_found[offset]

                playlist_list = []
                for playlist_info in playlists_found:
                    # catch the tracklist
                    track_list_url = playlist_info["tracks"]["href"]
                    track_response = requests.get(track_list_url, headers=headers)
                    track_response.raise_for_status()
                    track_info = track_response.json()
                    track_list = [
                        Track(
                            track_name=item["track"]["name"],
                            artist_name=item["track"]["artists"][0]["name"],
                            album_name=item["track"]["album"]["name"],
                        )
                        for item in track_info["items"]
                    ]
                    # create a playlist object
                    found_playlist = Playlist(
                        playlist_name=playlist_info["name"],
                        playlist_url=playlist_info["external_urls"]["spotify"],
                        track_list=track_list,
                    )
                    playlist_list.append(found_playlist)

                self.playlists.extend(playlist_list)

                return playlist_list

            else:
                raise HTTPException(status_code=404, detail="Playlist not found")
        except requests.exceptions.HTTPError as err:
            raise HTTPException(status_code=err.response.status_code, detail=str(err))



class AlbumManager:
    def __init__(self) -> None:
        self.album_list = []
        self.token = get_token()
    
    def get_albums_from_artist(self, artist_name: str, offset: int = 0, limit: int = 5) -> list[Album]:
        url = f"https://api.spotify.com/v1/search"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {
            "q": artist_name,
            "type": "album",
            "limit": limit,
            "offset": offset,
        }  
        response = requests.get(url, headers=headers, params=params)
        try:
            response.raise_for_status()
            album_data = response.json()
            album_list_data = album_data.get("albums", {}).get("items", [])
            albums = TypeAdapter(List[Album]).validate_python(album_list_data)
                                                
            return albums
        except requests.exceptions.HTTPError as err:
            raise HTTPException(status_code=err.response.status_code, detail=str(err))
            
            
if __name__ == "__main__":
    manager = AlbumManager()
    result = manager.get_albums_from_artist("rick astley")
    print(result)