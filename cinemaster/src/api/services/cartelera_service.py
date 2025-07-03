from models.database import Pelicula, Funcion, HorarioAsientos

class CarteleraService:
    @staticmethod
    def listar_peliculas(db):
        peliculas = db.query(Pelicula).all()
        return [
            {
                "id": p.id_pelicula,
                "Title": p.Title,
                "Duration": p.Duration,
                "Gender": p.Gender,
                "Image_path": p.Image_path
            }
            for p in peliculas
        ]
    
    @staticmethod
    def obtener_horarios(db, pelicula_id):
        """Obtiene los horarios de una película específica"""
        horarios = db.query(Funcion).filter(Funcion.id_pelicula == pelicula_id).all()
        return [
            {
                "id": h.id_funcion,
                "fecha": h.Schedule.isoformat() if h.Schedule else None
            }
            for h in horarios
        ]
    
    @staticmethod
    def obtener_asientos_disponibles(db, horario_id):
        """Obtiene los asientos disponibles para un horario específico"""
        horario_asientos = db.query(HorarioAsientos)\
            .filter(HorarioAsientos.horario_id == horario_id, HorarioAsientos.Available == True).all()
        
        asientos_disponibles = []
        for ha in horario_asientos:
            if ha.asiento:
                asientos_disponibles.append({
                    "id": ha.asiento.ids_seats,
                    "nombre": ha.asiento.ids_seats
                })
        
        return asientos_disponibles