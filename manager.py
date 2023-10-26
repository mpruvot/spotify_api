import json
from fastapi import HTTPException
import requests
from models import Playlist, Track, Album
from auth import get_token
from pydantic import TypeAdapter
from typing import List

