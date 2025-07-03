class PeliculaAdapter:
    """Adapta datos de API a formato compatible con CartelClasico"""
    
    def __init__(self, api_data, cartelera_view=None):
        # La API devuelve 'pelicula_id', no 'id'
        self.id_pelicula = api_data.get('pelicula_id')
        self.Title = api_data.get('titulo')  # La API devuelve 'titulo'
        self.Duration = api_data.get('duracion')  # La API devuelve 'duracion'
        self.Gender = api_data.get('genero')  # La API devuelve 'genero'
        self.Image_path = api_data.get('Image_path')
        
        # Obtener horarios inmediatamente si se proporciona cartelera_view
        if cartelera_view and self.id_pelicula:
            horarios_api = cartelera_view.get_horarios_from_api(self.id_pelicula)
            from adapters.horario_adapter import HorarioAPI
            self.horarios = [HorarioAPI(horario_id, fecha) for horario_id, fecha in horarios_api]
        else:
            self.horarios = []  # CartelClasico espera esto, se carga después en reservation_view
        
        # Debug para ver qué datos llegan
        print(f"🔍 PeliculaAdapter creado: ID={self.id_pelicula}, Título={self.Title}, Horarios={len(self.horarios)}")
    
    @classmethod
    def from_api_list(cls, api_data_list, cartelera_view=None):
        """Convierte una lista de datos de API a objetos compatibles"""
        print(f"🔍 Creando adaptadores para {len(api_data_list)} películas")
        return [cls(data, cartelera_view) for data in api_data_list]