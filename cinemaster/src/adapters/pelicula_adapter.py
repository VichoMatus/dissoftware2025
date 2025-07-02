class PeliculaAdapter:
    """Adapta datos de API a formato compatible con CartelClasico"""
    
    def __init__(self, api_data):
        self.id_pelicula = api_data.get('id')
        self.Title = api_data.get('Title')
        self.Duration = api_data.get('Duration')
        self.Gender = api_data.get('Gender')
        self.Image_path = api_data.get('Image_path')
        self.horarios = []  # CartelClasico espera esto, se carga después en reservation_view
    
    @classmethod
    def from_api_list(cls, api_data_list):
        """Convierte una lista de datos de API a objetos compatibles"""
        return [cls(data) for data in api_data_list]