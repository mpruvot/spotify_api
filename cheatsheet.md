# Spotify API et FastAPI Cheat Sheet

## Environnement et dépendances

```bash
pip install fastapi
pip install requests
pip install python-dotenv
```

## Import des bibliothèques

```python
from dotenv import load_dotenv
import os
from fastapi import FastAPI
import json
import base64
import requests
```

## Chargement des variables d'environnement

Créez un fichier `.env` contenant les informations sensibles :

```
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
```

Puis chargez ces variables :

```python
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
```

## Authentification avec Spotify

### Concaténation des identifiants

```python
client_creds = f"{client_id}:{client_secret}"
```

### Encodage en Base64

```python
client_creds_b64 = base64.b64encode(client_creds.encode()).decode()
```

### Configuration des headers pour la requête

```python
token_headers = {"Authorization": f"Basic {client_creds_b64}"}
```

### Données pour la requête POST

```python
token_data = {"grant_type": "client_credentials"}
```

### Envoyer la requête POST et obtenir le token

```python
r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)

if r.status_code == 200:
    token_info = r.json()
    token = token_info['access_token']
else:
    token = None
```

## Utilisation du token pour accéder à l'API de Spotify

Vous pouvez maintenant utiliser le token obtenu dans les headers de vos futures requêtes à l'API Spotify :

```python
headers = {"Authorization": f"Bearer {token}"}
```
