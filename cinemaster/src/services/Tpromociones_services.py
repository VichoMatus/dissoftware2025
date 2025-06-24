from sqlalchemy.orm import Session
from models.database import Promociones

class PromocionesService:
    @staticmethod
    def listar_promociones(db: Session):
        return db.query(Promociones).all()

    @staticmethod
    def crear_promocion(db: Session, Type, Membership):
        nueva = Promociones(
            Type=Type,
            Membership=Membership
        )
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return nueva

    @staticmethod
    def actualizar_promocion(db: Session, id_promotions, Type, Membership):
        promocion = db.query(Promociones).filter(Promociones.id_promotions == id_promotions).first()
        if promocion:
            promocion.Type = Type
            promocion.Membership = Membership
            db.commit()
            return promocion
        return None

    @staticmethod
    def eliminar_promocion(db: Session, id_promotions):
        promocion = db.query(Promociones).filter(Promociones.id_promotions == id_promotions).first()
        if promocion:
            db.delete(promocion)
            db.commit()
            return True