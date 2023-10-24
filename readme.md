# Spotify API Project
## Description
This project utilizes the Spotify API to fetch information about public playlists. It is built using FastAPI and interacts with the Spotify API to get details about playlists and tracks.
## Installation
1. Clone this repository:
```bash
git clone https://github.com/mpruvot/spotify_api.git
```
2. Navigate to the project folder:
```bash
cd spotify_api
```
3. Install the dependencies:
```bash
pip install -r requirements.txt
```
## Usage
1. Start the FastAPI server:
```bash
uvicorn main:app --reload
```
2. Navigate to the FastAPI user interface at `http://127.0.0.1:8000/docs`.
## Routes
- `GET /`: Home Page
- `GET /callback`: Test Access Token
- `GET /playlist/{playlist_name}`: Fetch Public Playlist Information
## Features
- Spotify Authentication
- Public Playlist Search
- Fetching Track Details of a Playlist
