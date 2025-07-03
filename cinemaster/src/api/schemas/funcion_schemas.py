from pydantic import BaseModel
from datetime import datetime

class FuncionCreate(BaseModel):
    id_pelicula: int
    employee_id: int
    Schedule: datetime