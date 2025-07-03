from pydantic import BaseModel
from typing import Optional

class EmpleadoBase(BaseModel):
    Name: str
    Email: str
    Password: str

class EmpleadoCreate(EmpleadoBase):
    pass

class EmpleadoUpdate(BaseModel):
    Name: Optional[str] = None
    Email: Optional[str] = None
    Password: Optional[str] = None

class EmpleadoResponse(BaseModel):
    employee_id: int
    Name: str
    Email: str
    
    class Config:
        from_attributes = True

class EmpleadoCloneRequest(BaseModel):
    Name: str
    Email: str
    Password: str
