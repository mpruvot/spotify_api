import json
import requests
from models import Playlist, Track
from auth import get_token


class PlaylistManager:
    def __init__(self) -> None:
        self.playlists = []
        self.token = get_token()

    def get_public_playlist(self, playlist_name: str) -> Playlist:
        url = f"https://api.spotify.com/v1/search"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {
            "q": playlist_name,
            "type": "playlist",
            "limit": 1,  # limits the results to one single playlist
        }
        response = requests.get(url, headers=headers, params=params)
        try:
            response.raise_for_status()
            search_results = response.json()
            
            if search_results['playlists']['total'] > 0:
                playlist_info = search_results['playlists']['items'][0]
                
                #catch the tracklist
                track_list_url = playlist_info['tracks']['href']
                track_response = requests.get(track_list_url, headers=headers)
                track_response.raise_for_status()
                track_info = track_response.json()
                track_list = [Track(track_name=item['track']['name'], artist_name=item['track']['artists'][0]['name'], album_name=item['track']['album']['name']) for item in track_info['items']]
                #create a playlist object
                found_playlist = Playlist(
                    playlist_name=playlist_info['name'],
                    playlist_url=playlist_info['external_urls']['spotify'],
                    track_list=track_list
                )
                #print(json.dumps(playlist_info, indent=6))
                return found_playlist
            else:
                return {"error" : "Playlist not Found"}
        except requests.exceptions.HTTPError as err:
            return {"error": f"An error occurred while fetching the playlist: {err}"} 
    
if __name__ == "__main__":
    manager = PlaylistManager()
    result = manager.get_public_playlist("Ambient Essentials")
    print(result)
