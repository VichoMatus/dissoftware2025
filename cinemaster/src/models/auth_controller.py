from sqlalchemy.orm import Session  # Asegúrate de importar Session desde sqlalchemy.orm
from models.database import SessionLocal  # Si estás usando la sesión local también
from models.database import Cliente, Empleado, Administrador  # Clase Cliente que representa la tabla de la base de datos

class AuthController:
    @staticmethod
    def register_cliente(db: Session, name: str, email: str, password: str, membership: bool):
        # Verificar si el cliente ya existe
        existing_cliente = db.query(Cliente).filter(Cliente.Email == email).first()
        if existing_cliente:
            raise ValueError("El correo electrónico ya está registrado.")
        
        # Crear nuevo cliente
        cliente = Cliente(
            nombre=name,  # Asegúrate de que el campo sea 'Name'
            Email=email,  # Asegúrate de que el campo sea 'Email'
            Password=password,  # Asegúrate de que el campo sea 'Password'
            Membership=membership,  # Asegúrate de que el campo sea 'Membership'
            Reservation_history=""  # Campo opcional para historial de reservas
        )
        
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        return cliente

    @staticmethod
    def login_cliente(db: Session, email: str, password: str):
        # Asegúrate de que la columna que consultas sea 'Email' y 'Password'
        cliente = db.query(Cliente).filter(Cliente.Email == email, Cliente.Password == password).first()
        return cliente
    

    @staticmethod
    def register_employee(db: Session, name: str, email: str, password: str):
        existing_employee = db.query(Empleado).filter(Empleado.Email == email).first()  # Llamar a 'first' correctamente
        if existing_employee:
            raise ValueError("El correo electrónico ya está registrado.")
        
        # Crear nuevo empleado
        empleado = Empleado(
            nombre=name,
            Email=email,
            Password=password,            
        )

        db.add(empleado)    
        db.commit()
        db.refresh(empleado)
        return empleado
    
    @staticmethod
    def login_empleado(db: Session, email: str, password: str):
        empleado_e = db.query(Empleado).filter(Empleado.Email == email, Empleado.Password == password).first()  # Renombrado 'Empleado' a 'empleado'
        return empleado_e
    
    @staticmethod
    def login_admin(db: Session, email: str, password: str):
        # Asegúrate de que la columna que consultas sea 'Email' y 'Password'
        admin = db.query(Administrador).filter(Administrador.Email == email, Administrador.Password == password).first()
        return admin
