import json
from fastapi import HTTPException
import requests
from models import Playlist, Track
from auth import get_token


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


if __name__ == "__main__":
    manager = PlaylistManager()
    result = manager.get_public_playlist("rock", offset=0, limit=1)


    print(result)
