from pydantic import BaseModel

class ReservaCreate(BaseModel):
    client_id: int
    id_funcion: int
    employee_id: int