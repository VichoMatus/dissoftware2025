from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FuncionCreate(BaseModel):
    id_pelicula: int
    employee_id: int
    Schedule: datetime

class FuncionUpdate(BaseModel):
    id_pelicula: Optional[int] = None
    employee_id: Optional[int] = None
    Schedule: Optional[datetime] = None

class FuncionResponse(BaseModel):
    id_funcion: int
    id_pelicula: int
    employee_id: int
    Schedule: datetime
    pelicula_titulo: Optional[str] = None
    empleado_nombre: Optional[str] = None

class FuncionWithDetails(BaseModel):
    id_funcion: int
    id_pelicula: int
    employee_id: int
    Schedule: datetime
    pelicula_titulo: str
    pelicula_duracion: int
    pelicula_genero: str
    empleado_nombre: str
    empleado_email: str

class FuncionDeleteResponse(BaseModel):
    success: bool
    message: str
    id_funcion: int