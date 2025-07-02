from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import get_db
from services.Treservas_service import ReservaService

router = APIRouter(prefix="/reservas", tags=["Reservas"])
