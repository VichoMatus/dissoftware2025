from views.authentication.login_view import LoginView
from views.authentication.register_view import RegisterView
from views.cartelera_view import MainView
from views.trabajador_view import TrabajadorView
from views.admin_view import AdminView
from api.services.register_login import ApiAuthService, ApiRegistrationService, AuthServiceInterface, RegistrationServiceInterface, DashboardLogger

class AppController:
    """
    Controlador principal de la aplicación.
    
    Principios SOLID aplicados:
    - SRP: Solo maneja la navegación entre vistas
    - OCP: Extensible para nuevas vistas sin modificar código existente
    - LSP: Acepta cualquier implementación de los servicios
    - ISP: Depende solo de las interfaces necesarias
    - DIP: Depende de abstracciones (interfaces), no de implementaciones concretas
    """
    
    def __init__(self, 
                 auth_service: AuthServiceInterface = None, 
                 registration_service: RegistrationServiceInterface = None):
        """
        Constructor con inyección de dependencias
        
        Args:
            auth_service: Servicio de autenticación (inyectado)
            registration_service: Servicio de registro (inyectado)
        """
        # DIP: Usar servicios inyectados o crear por defecto
        self._auth_service = auth_service or ApiAuthService()
        self._registration_service = registration_service or ApiRegistrationService()
        self._dashboard_logger = DashboardLogger()
        
        # Verificar conexión con la API al inicializar
        self._check_api_connectivity()
    
    def start(self):
        """Inicia la aplicación mostrando la vista de login"""
        self.open_login_view()
    
    def open_register_view(self):
        """
        Abre la vista de registro
        SRP: Responsabilidad específica de navegación
        """
        app = RegisterView(self._registration_service, self.open_login_view)
        app.mainloop()
    
    def open_login_view(self):
        """
        Abre la vista de login
        SRP: Responsabilidad específica de navegación
        """
        app = LoginView(
            self._auth_service,
            self.open_register_view,
            self.open_cartelera_view,
            self.open_trabajador_view,
            self.open_admin_view
        )
        app.mainloop()
    
    def open_cartelera_view(self, cliente):
        """
        Abre la vista de cartelera para clientes
        SRP: Responsabilidad específica de navegación
        """
        # Establecer cliente en el dashboard de la API
        try:
            self._dashboard_logger.set_current_client(
                cliente.nombre, 
                cliente.cliente_id, 
                cliente.Email
            )
            # Registrar que está viendo la cartelera
            self._dashboard_logger.log_cartelera_view()
        except Exception as e:
            print(f"No se pudo establecer cliente en dashboard: {e}")
        
        # Crear vista de cartelera con logger
        app = MainView(cliente, self._dashboard_logger)
        app.mainloop()
    
    def open_trabajador_view(self, employee_name):
        app = TrabajadorView(employee_name)
        app.mainloop()
    
    def open_admin_view(self):
        """
        Abre la vista de administrador
        SRP: Responsabilidad específica de navegación
        """
        app = AdminView()
        app.mainloop()
    
    def _check_api_connectivity(self):
        """
        Verifica la conectividad con la API
        SRP: Responsabilidad específica de verificación
        """
        if not self._auth_service.test_connection():
            print("⚠️  Advertencia: No se pudo conectar con la API.")
            print("   Asegúrate de que la API esté ejecutándose en http://127.0.0.1:8000")
            print("   Algunas funciones pueden no funcionar correctamente.")
