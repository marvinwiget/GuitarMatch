from pydantic import BaseModel
from typing import Optional

class SongMetaData(BaseModel):
    id: str
    title: str
    artist: str
    album_art: str
    spotify_url: str

class SongEvaluation(BaseModel):
    guitar_friendly: bool
    difficulty: str  # beginner, intermediate, advanced, N/A
    tuning: str      # e.g. Standard
    info: str
    tab_url: Optional[str] = None

class EvaluatedSong(SongMetaData):
    evaluation: SongEvaluation