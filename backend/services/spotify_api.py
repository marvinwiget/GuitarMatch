import os
import httpx
import secrets

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8000/auth/callback")

USER_TOKENS = set()

def authorization():
    scope = "user-read-recently-played"
    state = secrets.token_urlsafe(16)
    USER_TOKENS.add(state)

    config = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "state": state,
        "scope": scope,
        "show_dialog": "true"
    }
    auth_url = httpx.URL("https://accounts.spotify.com/authorize", params=config)
    return str(auth_url)

async def callback(code: str):
    token_url = "https://accounts.spotify.com/api/token"
    
    options = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }
    
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=options, headers=headers)
        
    if response.status_code != 200:
        raise Exception(f"Failed to get token from Spotify: {response.text}")
        
    return response.json()