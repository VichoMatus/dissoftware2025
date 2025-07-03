from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, time

class PeliculaResponse(BaseModel):
    pelicula_id: int
    titulo: str
    genero: Optional[str] = None
    duracion: Optional[int] = None
    image_path: Optional[str] 

class HorarioResponse(BaseModel):
    horario_id: int
    pelicula_id: int
    sala_id: int
    fecha: str
    hora_inicio: str
    hora_fin: Optional[str] = None
    estado: str

class AsientoResponse(BaseModel):
    asiento_id: str  # Cambiado de int a str porque los IDs son como 'A1', 'A2', etc.
    numero_asiento: str
    fila: str
    sala_id: int
    disponible: bool
