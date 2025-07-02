from pydantic import BaseModel, Field
from typing import Optional, Union

class ReservaCreate(BaseModel):
    client_id: int
    id_funcion: int
    employee_id: int

class ReservaRequest(BaseModel):
    client_id: int = Field(..., example=5, description="ID del cliente en el sistema")
    id_funcion: int = Field(..., example=1, description="ID de la función/horario seleccionado")
    seat_id: str = Field(..., example="A5", description="Identificador del asiento seleccionado")
    movie_name: str = Field(..., example="Bajoterra", description="Nombre de la película")
    showtime_string: str = Field(..., example="2025-05-30 23:00", description="Horario de la función")
    imagen: Optional[str] = Field(None, example="/path/to/bajoterra.jpg", description="Ruta de la imagen de la película")
    cliente_nombre: str = Field(..., example="Seba", description="Nombre completo del cliente")
    costo_entrada: float = Field(..., example=12.0, description="Precio de la entrada")
    metodo_pago: str = Field(..., example="tarjeta", description="Método de pago utilizado")
    cliente_email: Optional[str] = Field(None, example="spereda2024@alu.uct.cl", description="Email del cliente para confirmación")

class ReservaResponse(BaseModel):
    success: bool = Field(..., example=True, description="Indica si la reserva fue exitosa")
    message: str = Field(..., example="Reserva confirmada exitosamente. Boleta generada y email enviado.", description="Mensaje descriptivo del resultado")
    reserva_id: Optional[Union[int, str]] = Field(None, example="b058dd05-7b18-4edb-8713-e77cb3897a7a", description="ID de la reserva creada (puede ser entero o UUID)")

class ReservaListResponse(BaseModel):
    reserva_id: str
    cliente_id: int
    cliente_nombre: str
    movie_name: str
    showtime_string: str
    seat_id: str
    costo_entrada: float
    fecha_reserva: str