class HorarioAPI:
    """Clase simple para representar horarios que vienen de la API"""
    def __init__(self, horario_id, fecha):
        self.id = horario_id
        self.fecha = fecha
    
    def __repr__(self):
        return f"HorarioAPI(id={self.id}, fecha={self.fecha})"
