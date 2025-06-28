from models.database import Pelicula

class CarteleraService:
    @staticmethod
    def listar_peliculas(db):
        return db.query(Pelicula).all()