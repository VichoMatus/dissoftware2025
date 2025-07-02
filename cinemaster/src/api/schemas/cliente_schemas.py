from pydantic import BaseModel

class ClienteCreate(BaseModel):
    nombre: str
    Email: str
    Password: str