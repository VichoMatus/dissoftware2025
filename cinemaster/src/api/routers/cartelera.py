from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from api.database import get_db
from api.schemas.cartelera_schemas import (
    PeliculaResponse,
    HorarioResponse, 
    AsientoResponse
)

router = APIRouter(prefix="/cartelera", tags=["Cartelera"])

@router.get("/", response_model=List[PeliculaResponse])
def listar_cartelera(db: Session = Depends(get_db)):
    """
    Devuelve la lista de todas las películas en cartelera con todos sus datos.
    """
    query = text("""
        SELECT id_pelicula, Title, Gender, Duration, Image_path
        FROM Pelicula
        ORDER BY Title
    """)
    result = db.execute(query)
    
    peliculas = []
    for row in result:
        peliculas.append(PeliculaResponse(
            pelicula_id=row.id_pelicula,
            titulo=row.Title,
            genero=row.Gender,
            duracion=row.Duration,
            image_path=row.Image_path
        ))
    
    return peliculas


@router.get("/{pelicula_id}/horarios", response_model=List[HorarioResponse])
def obtener_horarios_pelicula(
    pelicula_id: int = Path(..., description="ID de la película", gt=0),
    db: Session = Depends(get_db)
):
    """Obtiene los horarios de una película específica"""
    try:
        print(f"🔍 API: Buscando horarios para película ID: {pelicula_id}")
        
        # Verificar que la película existe
        query_pelicula = text("SELECT id_pelicula FROM Pelicula WHERE id_pelicula = :pelicula_id")
        result_pelicula = db.execute(query_pelicula, {"pelicula_id": pelicula_id})
        pelicula = result_pelicula.fetchone()
        
        if not pelicula:
            print(f"❌ API: Película con ID {pelicula_id} no encontrada")
            raise HTTPException(
                status_code=404, 
                detail=f"No se encontró la película con ID {pelicula_id}"
            )
        
        print(f"✅ API: Película encontrada, buscando horarios...")
        
        query = text("""
            SELECT h.id as horario_id, h.pelicula_id, 0 as sala_id, 
                   h.fecha, h.fecha as hora_inicio, 
                   NULL as hora_fin, 'activo' as estado
            FROM Horario h 
            WHERE h.pelicula_id = :pelicula_id
            ORDER BY h.fecha
        """)
        result = db.execute(query, {"pelicula_id": pelicula_id})
        
        horarios = []
        for row in result:
            horarios.append(HorarioResponse(
                horario_id=row.horario_id,
                pelicula_id=row.pelicula_id,
                sala_id=row.sala_id,
                fecha=str(row.fecha),
                hora_inicio=str(row.hora_inicio),
                hora_fin=str(row.hora_fin) if row.hora_fin else None,
                estado=row.estado
            ))
        
        print(f"✅ API: Encontrados {len(horarios)} horarios")
        return horarios
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ API: Error inesperado en horarios: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error interno al obtener horarios: {str(e)}"
        )


@router.get("/horarios/{horario_id}/asientos", response_model=List[AsientoResponse])
def obtener_asientos_disponibles(
    horario_id: int = Path(..., description="ID del horario", gt=0),
    db: Session = Depends(get_db)
):
    """Obtiene los asientos disponibles para un horario específico"""
    try:
        print(f"🔍 API: Buscando asientos para horario ID: {horario_id}")
        
        # Primero verificar que el horario existe
        query_horario = text("SELECT id, pelicula_id FROM Horario WHERE id = :horario_id")
        result = db.execute(query_horario, {"horario_id": horario_id})
        horario = result.fetchone()
        
        if not horario:
            print(f"❌ API: Horario con ID {horario_id} no encontrado")
            raise HTTPException(
                status_code=404, 
                detail=f"No se encontró el horario con ID {horario_id}"
            )
        
        print(f"✅ API: Horario encontrado, buscando asientos...")
        
        # Obtener asientos con su disponibilidad para este horario específico
        query = text("""
            SELECT 
                a.ids_seats as asiento_id,
                a.ids_seats as numero_asiento,
                SUBSTR(a.ids_seats, 1, 1) as fila,
                COALESCE(a.id_Hall, 1) as sala_id,
                COALESCE(ha.Available, 1) as disponible
            FROM Asiento a
            LEFT JOIN horario_asientos ha ON a.ids_seats = ha.asiento_id 
                                          AND ha.horario_id = :horario_id
            ORDER BY a.ids_seats
        """)
        result = db.execute(query, {"horario_id": horario_id})
        
        asientos = []
        for row in result:
            asientos.append(AsientoResponse(
                asiento_id=row.asiento_id,
                numero_asiento=row.numero_asiento,
                fila=row.fila,
                sala_id=row.sala_id,
                disponible=bool(row.disponible)
            ))
        
        print(f"✅ API: Encontrados {len(asientos)} asientos para horario {horario_id}")
        return asientos
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ API: Error inesperado al obtener asientos: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error interno al obtener asientos: {str(e)}"
        )


@router.get("/debug/info")
def debug_info(db: Session = Depends(get_db)):
    """Endpoint de debugging para diagnosticar problemas de la API"""
    try:
        # Información de películas
        query_peliculas = text("SELECT id_pelicula, Title FROM Pelicula")
        result_peliculas = db.execute(query_peliculas)
        peliculas = [{"id": row.id_pelicula, "titulo": row.Title} for row in result_peliculas]
        
        # Información de horarios
        query_horarios = text("SELECT id, pelicula_id, fecha FROM Horario")
        result_horarios = db.execute(query_horarios)
        horarios = [{"horario_id": row.id, "pelicula_id": row.pelicula_id, "fecha": str(row.fecha)} for row in result_horarios]
        
        # Información de asientos y horario_asientos
        query_asientos = text("SELECT COUNT(*) as total FROM Asiento")
        result_asientos = db.execute(query_asientos)
        total_asientos = result_asientos.fetchone().total
        
        query_ha = text("SELECT COUNT(*) as total FROM horario_asientos")
        result_ha = db.execute(query_ha)
        total_horario_asientos = result_ha.fetchone().total
        
        return {
            "peliculas_disponibles": peliculas,
            "horarios_disponibles": horarios,
            "total_asientos": total_asientos,
            "total_horario_asientos": total_horario_asientos,
            "rutas_validas": {
                "obtener_cartelera": "/cartelera/",
                "obtener_horarios": [f"/cartelera/{p['id']}/horarios" for p in peliculas],
                "obtener_asientos": [f"/cartelera/horarios/{h['horario_id']}/asientos" for h in horarios]
            },
            "mensaje": "Usa estas rutas para acceder a la información"
        }
    except Exception as e:
        return {"error": str(e), "tipo_error": type(e).__name__}