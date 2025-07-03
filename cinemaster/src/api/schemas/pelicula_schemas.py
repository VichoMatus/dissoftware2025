from pydantic import BaseModel
from typing import Optional

class PeliculaCreate(BaseModel):
    Title: str
    Duration: int
    Gender: str | None = None
    Image_path: str

class PeliculaResponse(BaseModel):
    id_pelicula: int
    Title: str
    Duration: int
    Gender: Optional[str] = None
    Image_path: Optional[str] = None

class PeliculaSimple(BaseModel):
    """Schema simplificado para dropdowns y listas"""
    id_pelicula: int
    Title: str