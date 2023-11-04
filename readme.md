# Spotify API Wrapper

This repository contains a Python project that serves as a wrapper for the Spotify Web API. It allows users to search for various Spotify entities such as artists, albums, tracks, and playlists.

## Features

- Search for artists, albums, tracks, and playlists by name.
- Retrieve detailed information about the searched entity.
- Docker support for easy deployment and isolation.
- Automated tests for validation of the endpoints.

## Getting Started

To get started with this project, clone the repository and install the required dependencies.

### Prerequisites

- Python 3.11.5 or higher
- Docker (optional for containerization)

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/mpruvot/spotify_api.git
   ```
2. Install the required Python packages:
   ```sh
   pip install -r requirements.txt
   ```

### Usage

Run the application locally by executing:

```sh
uvicorn spotify_api.main:app --reload
```

The API will be available at `http://localhost:8000`.

### Docker

Alternatively, you can use Docker to build and run the application:

```sh
docker-compose up --build
```

## Endpoints

The following endpoints are available:

- `GET /`: Returns a welcome message.
- `GET /artist/{name}`: Retrieves an artist by name.
- `GET /album/{name}`: Retrieves an album by name.
- `GET /track/{name}`: Retrieves a track by name.
- `GET /playlist/{name}`: Retrieves a playlist by name.

## Testing

Automated tests are provided to ensure the functionality of the endpoints. Run the tests using:

```sh
pytest
```

## Files

- `Dockerfile`: Defines the Docker container setup.
- `docker-compose.yml`: Docker Compose configuration for orchestrating the container.
- `requirements.txt`: Lists all the Python dependencies.
- `spotify_api/main.py`: The FastAPI application entry point.
- `spotify_api/manager.py`: Contains the logic for interacting with the Spotify API.
- `spotify_api/models.py`: Pydantic models for type validation.
- `spotify_api/oauth.py`: Handles OAuth authentication with Spotify.
- `tests/test_main.py`: Tests for the main application.
- `tests/test_token.py`: Tests for the OAuth token retrieval.



## Acknowledgments

- This project utilizes the FastAPI framework for creating a web API.
- Authentication with Spotify is done via OAuth 2.0.

