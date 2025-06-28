from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

# --- [CORRECCIÓN AQUÍ] ---
# La importación ahora es absoluta desde la raíz del paquete (la carpeta 'src')
from models.database import SessionLocal, Cliente, Reserva_asientos, Reserva, Funcion, Pelicula, Asiento
from services.cliente_services import ClienteService

# --- Modelos Pydantic para validar los datos de entrada/salida ---

class ClientUpdateRequest(BaseModel):
    nombre: str
    email: str
    password: str

class ReservationResponse(BaseModel):
    reservation_id: int
    pelicula: str
    fecha: str
    asientos: str

# --- Router de FastAPI ---
router = APIRouter(
    prefix="/profile",
    tags=["Client Profile"]
)

# --- Dependencia para la sesión de la base de datos ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints ---

@router.put("/update/{client_id}", status_code=200)
def update_client_data(client_id: int, client_data: ClientUpdateRequest, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un cliente.
    """
    if len(client_data.password) < 4:
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 4 caracteres.")

    cliente_db = db.query(Cliente).filter(Cliente.cliente_id == client_id).first()
    if not cliente_db:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    try:
        cliente_db.nombre = client_data.nombre
        cliente_db.Email = client_data.email
        cliente_db.Password = client_data.password  # En producción, esto debería ser hasheado
        db.commit()
        return {"message": "Datos actualizados correctamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ocurrió un error en el servidor: {e}")

@router.get("/{client_id}/reservations", response_model=List[ReservationResponse])
def get_client_reservations(client_id: int, historical: bool = False, db: Session = Depends(get_db)):
    """
    Obtiene las reservas de un cliente (actuales o del historial).
    """
    cliente_db = db.query(Cliente).filter(Cliente.cliente_id == client_id).first()
    if not cliente_db:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    reservas_db = ClienteService.obtener_historial_reservas(cliente_db) if historical else ClienteService.obtener_reservas_actuales(cliente_db)

    response_list = []
    for r in reservas_db:
        asientos_obj = db.query(Reserva_asientos).filter(Reserva_asientos.reservation_id == r.reservation_id).all()
        lista_asientos = ", ".join([a.asiento.ids_seats for a in asientos_obj]) if asientos_obj else "Pendiente"
        
        response_list.append(ReservationResponse(
            reservation_id=r.reservation_id,
            pelicula=r.funcion.pelicula.Title if r.funcion and r.funcion.pelicula else "N/A",
            fecha=r.funcion.Schedule.strftime("%Y-%m-%d %H:%M") if r.funcion else "N/A",
            asientos=lista_asientos
        ))
    return response_list

@router.delete("/reservations/cancel/{reservation_id}", status_code=200)
def cancel_reservation(reservation_id: int, db: Session = Depends(get_db)):
    """
    Cancela una reserva. (Implementar la lógica de negocio aquí).
    """
    reserva = db.query(Reserva).filter(Reserva.reservation_id == reservation_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    # Aquí iría tu lógica: cambiar estado, eliminar, etc.
    # Por ahora, simulamos el éxito.
    # db.delete(reserva)
    # db.commit()
    
    return {"message": f"Reserva {reservation_id} cancelada."}