import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

import backend.services.spotify_api as spotify_api

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return {"status": "online"}

@app.get("/auth/login")
async def login():
    auth_uri = spotify_api.authorization()
    return RedirectResponse(url=auth_uri)

@app.get("/auth/callback")
async def callback(code: str, state: str):
    if state not in spotify_api.USER_TOKENS:
        raise HTTPException(status_code=400, detail="State does not match")
    spotify_api.USER_TOKENS.remove(state)

    try:
        token_data = await spotify_api.callback(code)
        access_token = token_data.get("access_token")
        
        return {
            "status": "Authenticated Successfully!",
            "access_token": access_token,
            "expires_in": token_data.get("expires_in"),
            "token_type": token_data.get("token_type")
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

