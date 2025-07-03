from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    user_type: Optional[str] = None
    user_data: Optional[dict] = None

class RegisterRequest(BaseModel):
    email: str
    password: str
    nombre: Optional[str] = None

class RegisterResponse(BaseModel):
    success: bool
    message: str
    cliente: dict
