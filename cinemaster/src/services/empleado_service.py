from models.employee import Empleado
from sqlalchemy.orm import Session
from typing import List, Optional, Protocol

class IEmpleadoCRUD(Protocol):
    def agregar_empleado(self, nombre: str, email: str, password: str) -> Empleado: ...
    def listar_empleados(self) -> List[Empleado]: ...
    def obtener_empleado(self, empleado_id: int) -> Optional[Empleado]: ...
    def actualizar_empleado(self, empleado_id: int, nombre: str, email: str, password: str) -> Optional[Empleado]: ...
    def eliminar_empleado(self, empleado_id: int) -> bool: ...

class EmpleadoService(IEmpleadoCRUD):
    def __init__(self, db_session: Session):
        self.db = db_session

    def agregar_empleado(self, nombre: str, email: str, password: str) -> Empleado:
        emp = Empleado(Name=nombre, Email=email, Password=password)
        self.db.add(emp)
        self.db.commit()
        self.db.refresh(emp)
        return emp

    def listar_empleados(self) -> List[Empleado]:
        return self.db.query(Empleado).all()

    def obtener_empleado(self, empleado_id: int) -> Optional[Empleado]:
        return self.db.query(Empleado).get(empleado_id)

    def actualizar_empleado(self, empleado_id: int, nombre: str, email: str, password: str) -> Optional[Empleado]:
        emp = self.db.query(Empleado).get(empleado_id)
        if emp:
            emp.Name = nombre
            emp.Email = email
            emp.Password = password
            self.db.commit()
            self.db.refresh(emp)
            return emp
        return None

    def eliminar_empleado(self, empleado_id: int) -> bool:
        emp = self.db.query(Empleado).get(empleado_id)
        if emp:
            self.db.delete(emp)
            self.db.commit()
            return True
        return False