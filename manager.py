import json
from models import Playlist, Track

class PlaylistManager():
    def __init__(self) -> None:
        self.playlists = []
    
    def create_playlist(self)-> Playlist:
        pass