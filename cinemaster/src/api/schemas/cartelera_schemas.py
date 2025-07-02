from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, time

class PeliculaResponse(BaseModel):
    pelicula_id: int
    titulo: str
    genero: Optional[str] = None
    duracion: Optional[int] = None
    clasificacion: Optional[str] = None
    sinopsis: Optional[str] = None
    director: Optional[str] = None
    actores: Optional[str] = None
    fecha_estreno: Optional[str] = None
    precio: Optional[float] = None

class HorarioResponse(BaseModel):
    horario_id: int
    pelicula_id: int
    sala_id: int
    fecha: str
    hora_inicio: str
    hora_fin: Optional[str] = None
    estado: str

class AsientoResponse(BaseModel):
    asiento_id: int
    numero_asiento: str
    fila: str
    sala_id: int
    disponible: bool
