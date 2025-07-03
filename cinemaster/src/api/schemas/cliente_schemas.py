from pydantic import BaseModel
from typing import Optional

class ClienteBase(BaseModel):
    nombre: str
    Email: str
    Password: str

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    Email: Optional[str] = None
    Password: Optional[str] = None

class ClienteResponse(BaseModel):
    cliente_id: int
    nombre: str
    Email: str
    Membership: bool
    
    class Config:
        from_attributes = True

class ClienteCloneRequest(BaseModel):
    nombre: str
    Email: str
    Password: str