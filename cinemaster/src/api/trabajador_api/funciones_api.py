from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from api.database import get_db
from api.schemas.funcion_schemas import (
    FuncionCreate, 
    FuncionUpdate, 
    FuncionResponse, 
    FuncionWithDetails,
    FuncionDeleteResponse
)
from api.schemas.pelicula_schemas import PeliculaSimple

router = APIRouter(prefix="/funciones", tags=["Funciones"])

@router.get("/peliculas-disponibles", response_model=List[PeliculaSimple])
def obtener_peliculas_disponibles(db: Session = Depends(get_db)):
    """Obtiene lista de películas disponibles para usar en dropdowns"""
    try:
        query = text("SELECT id_pelicula, Title FROM Pelicula ORDER BY Title ASC")
        result = db.execute(query).fetchall()
        
        peliculas = []
        for row in result:
            peliculas.append(PeliculaSimple(
                id_pelicula=row.id_pelicula,
                Title=row.Title
            ))
        
        return peliculas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener películas: {str(e)}")

@router.get("/", response_model=List[FuncionResponse])
def listar_funciones(db: Session = Depends(get_db)):
    """Obtiene todas las funciones con información básica de película y empleado"""
    try:
        query = text("""
            SELECT 
                f.id_funcion,
                f.id_pelicula,
                f.employee_id,
                f.Schedule,
                p.Title as pelicula_titulo,
                e.Name as empleado_nombre
            FROM Funcion f
            LEFT JOIN Pelicula p ON f.id_pelicula = p.id_pelicula
            LEFT JOIN Empleado e ON f.employee_id = e.employee_id
            ORDER BY f.Schedule ASC
        """)
        result = db.execute(query).fetchall()
        
        funciones = []
        for row in result:
            funciones.append(FuncionResponse(
                id_funcion=row.id_funcion,
                id_pelicula=row.id_pelicula,
                employee_id=row.employee_id,
                Schedule=row.Schedule,
                pelicula_titulo=row.pelicula_titulo,
                empleado_nombre=row.empleado_nombre
            ))
        
        return funciones
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar funciones: {str(e)}")

@router.get("/{id_funcion}", response_model=FuncionWithDetails)
def obtener_funcion(id_funcion: int, db: Session = Depends(get_db)):
    """Obtiene una función específica con todos los detalles"""
    try:
        query = text("""
            SELECT 
                f.id_funcion,
                f.id_pelicula,
                f.employee_id,
                f.Schedule,
                p.Title as pelicula_titulo,
                p.Duration as pelicula_duracion,
                p.Gender as pelicula_genero,
                e.Name as empleado_nombre,
                e.Email as empleado_email
            FROM Funcion f
            LEFT JOIN Pelicula p ON f.id_pelicula = p.id_pelicula
            LEFT JOIN Empleado e ON f.employee_id = e.employee_id
            WHERE f.id_funcion = :id_funcion
        """)
        result = db.execute(query, {"id_funcion": id_funcion}).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Función no encontrada")
        
        return FuncionWithDetails(
            id_funcion=result.id_funcion,
            id_pelicula=result.id_pelicula,
            employee_id=result.employee_id,
            Schedule=result.Schedule,
            pelicula_titulo=result.pelicula_titulo,
            pelicula_duracion=result.pelicula_duracion,
            pelicula_genero=result.pelicula_genero,
            empleado_nombre=result.empleado_nombre,
            empleado_email=result.empleado_email
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener función: {str(e)}")

@router.post("/", response_model=FuncionResponse)
def crear_funcion(funcion: FuncionCreate, db: Session = Depends(get_db)):
    """Crea una nueva función con horario y asientos automáticamente"""
    try:
        # Verificar que la película existe
        pelicula_query = text("SELECT id_pelicula FROM Pelicula WHERE id_pelicula = :id_pelicula")
        pelicula_result = db.execute(pelicula_query, {"id_pelicula": funcion.id_pelicula}).fetchone()
        if not pelicula_result:
            raise HTTPException(status_code=400, detail="La película especificada no existe")
        
        # Verificar que el empleado existe
        empleado_query = text("SELECT employee_id FROM Empleado WHERE employee_id = :employee_id")
        empleado_result = db.execute(empleado_query, {"employee_id": funcion.employee_id}).fetchone()
        if not empleado_result:
            raise HTTPException(status_code=400, detail="El empleado especificado no existe")
        
        # Crear la función
        insert_funcion_query = text("""
            INSERT INTO Funcion (id_pelicula, employee_id, Schedule)
            VALUES (:id_pelicula, :employee_id, :Schedule)
        """)
        db.execute(insert_funcion_query, {
            "id_pelicula": funcion.id_pelicula,
            "employee_id": funcion.employee_id,
            "Schedule": funcion.Schedule
        })
        
        # Obtener el ID de la función creada
        last_funcion_id_query = text("SELECT last_insert_rowid() as id_funcion")
        last_funcion_id_result = db.execute(last_funcion_id_query).fetchone()
        id_funcion = last_funcion_id_result.id_funcion
        
        # Crear entrada en tabla Horario
        insert_horario_query = text("""
            INSERT INTO Horario (fecha, pelicula_id)
            VALUES (:fecha, :pelicula_id)
        """)
        db.execute(insert_horario_query, {
            "fecha": funcion.Schedule,
            "pelicula_id": funcion.id_pelicula
        })
        
        # Obtener el ID del horario creado
        last_horario_id_query = text("SELECT last_insert_rowid() as horario_id")
        last_horario_id_result = db.execute(last_horario_id_query).fetchone()
        horario_id = last_horario_id_result.horario_id
        
        # Crear asientos de A1 to E8 (5 filas x 8 columnas = 40 asientos)
        filas = ['A', 'B', 'C', 'D', 'E']
        columnas = range(1, 9)  # 1 a 8
        
        # Verificar que los asientos base existen en la tabla Asiento
        for fila in filas:
            for columna in columnas:
                asiento_id = f"{fila}{columna}"
                
                # Verificar si el asiento existe en la tabla Asiento
                check_asiento_query = text("SELECT ids_seats FROM Asiento WHERE ids_seats = :asiento_id")
                asiento_exists = db.execute(check_asiento_query, {"asiento_id": asiento_id}).fetchone()
                
                # Si no existe el asiento base, crearlo
                if not asiento_exists:
                    insert_asiento_base_query = text("""
                        INSERT INTO Asiento (ids_seats, id_Hall)
                        VALUES (:asiento_id, NULL)
                    """)
                    db.execute(insert_asiento_base_query, {"asiento_id": asiento_id})
                
                # Crear la relación horario-asiento con disponibilidad = 1 (disponible)
                insert_horario_asiento_query = text("""
                    INSERT INTO horario_asientos (horario_id, asiento_id, Available)
                    VALUES (:horario_id, :asiento_id, 1)
                """)
                db.execute(insert_horario_asiento_query, {
                    "horario_id": horario_id,
                    "asiento_id": asiento_id
                })
        
        # Confirmar todas las transacciones
        db.commit()
        
        # Obtener la función creada con detalles
        detail_query = text("""
            SELECT 
                f.id_funcion,
                f.id_pelicula,
                f.employee_id,
                f.Schedule,
                p.Title as pelicula_titulo,
                e.Name as empleado_nombre
            FROM Funcion f
            LEFT JOIN Pelicula p ON f.id_pelicula = p.id_pelicula
            LEFT JOIN Empleado e ON f.employee_id = e.employee_id
            WHERE f.id_funcion = :id_funcion
        """)
        result = db.execute(detail_query, {"id_funcion": id_funcion}).fetchone()
        
        print(f"✅ Función creada exitosamente:")
        print(f"   - ID Función: {id_funcion}")
        print(f"   - ID Horario: {horario_id}")
        print(f"   - Asientos creados: A1-E8 (40 asientos)")
        
        return FuncionResponse(
            id_funcion=result.id_funcion,
            id_pelicula=result.id_pelicula,
            employee_id=result.employee_id,
            Schedule=result.Schedule,
            pelicula_titulo=result.pelicula_titulo,
            empleado_nombre=result.empleado_nombre
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear función: {str(e)}")

@router.put("/{id_funcion}", response_model=FuncionResponse)
def actualizar_funcion(id_funcion: int, funcion: FuncionUpdate, db: Session = Depends(get_db)):
    """Actualiza una función existente"""
    try:
        # Verificar que la función existe
        check_query = text("SELECT id_funcion FROM Funcion WHERE id_funcion = :id_funcion")
        check_result = db.execute(check_query, {"id_funcion": id_funcion}).fetchone()
        if not check_result:
            raise HTTPException(status_code=404, detail="Función no encontrada")
        
        # Construir la consulta de actualización dinámicamente
        update_fields = []
        update_values = {"id_funcion": id_funcion}
        
        if funcion.id_pelicula is not None:
            # Verificar que la película existe
            pelicula_query = text("SELECT id_pelicula FROM Pelicula WHERE id_pelicula = :id_pelicula")
            pelicula_result = db.execute(pelicula_query, {"id_pelicula": funcion.id_pelicula}).fetchone()
            if not pelicula_result:
                raise HTTPException(status_code=400, detail="La película especificada no existe")
            update_fields.append("id_pelicula = :id_pelicula")
            update_values["id_pelicula"] = funcion.id_pelicula
        
        if funcion.employee_id is not None:
            # Verificar que el empleado existe
            empleado_query = text("SELECT employee_id FROM Empleado WHERE employee_id = :employee_id")
            empleado_result = db.execute(empleado_query, {"employee_id": funcion.employee_id}).fetchone()
            if not empleado_result:
                raise HTTPException(status_code=400, detail="El empleado especificado no existe")
            update_fields.append("employee_id = :employee_id")
            update_values["employee_id"] = funcion.employee_id
        
        if funcion.Schedule is not None:
            update_fields.append("Schedule = :Schedule")
            update_values["Schedule"] = funcion.Schedule
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No se proporcionaron campos para actualizar")
        
        # Ejecutar la actualización
        update_query = text(f"""
            UPDATE Funcion SET {', '.join(update_fields)}
            WHERE id_funcion = :id_funcion
        """)
        db.execute(update_query, update_values)
        db.commit()
        
        # Obtener la función actualizada con detalles
        detail_query = text("""
            SELECT 
                f.id_funcion,
                f.id_pelicula,
                f.employee_id,
                f.Schedule,
                p.Title as pelicula_titulo,
                e.Name as empleado_nombre
            FROM Funcion f
            LEFT JOIN Pelicula p ON f.id_pelicula = p.id_pelicula
            LEFT JOIN Empleado e ON f.employee_id = e.employee_id
            WHERE f.id_funcion = :id_funcion
        """)
        result = db.execute(detail_query, {"id_funcion": id_funcion}).fetchone()
        
        return FuncionResponse(
            id_funcion=result.id_funcion,
            id_pelicula=result.id_pelicula,
            employee_id=result.employee_id,
            Schedule=result.Schedule,
            pelicula_titulo=result.pelicula_titulo,
            empleado_nombre=result.empleado_nombre
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar función: {str(e)}")

@router.delete("/{id_funcion}", response_model=FuncionDeleteResponse)
def eliminar_funcion(id_funcion: int, db: Session = Depends(get_db)):
    """Elimina una función"""
    try:
        # Verificar que la función existe
        check_query = text("SELECT id_funcion FROM Funcion WHERE id_funcion = :id_funcion")
        check_result = db.execute(check_query, {"id_funcion": id_funcion}).fetchone()
        if not check_result:
            raise HTTPException(status_code=404, detail="Función no encontrada")
        
        # Verificar si hay reservas asociadas
        reservas_query = text("SELECT COUNT(*) as count FROM Reserva WHERE id_funcion = :id_funcion")
        reservas_result = db.execute(reservas_query, {"id_funcion": id_funcion}).fetchone()
        if reservas_result.count > 0:
            raise HTTPException(
                status_code=400, 
                detail="No se puede eliminar la función porque tiene reservas asociadas"
            )
        
        # Eliminar la función
        delete_query = text("DELETE FROM Funcion WHERE id_funcion = :id_funcion")
        db.execute(delete_query, {"id_funcion": id_funcion})
        db.commit()
        
        return FuncionDeleteResponse(
            success=True,
            message="Función eliminada exitosamente",
            id_funcion=id_funcion
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar función: {str(e)}")