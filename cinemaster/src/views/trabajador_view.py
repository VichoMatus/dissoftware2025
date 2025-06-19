import customtkinter as ctk
import webbrowser
from views.components.header_bar import HeaderBar
from views.components.side_bar_menu import SidebarMenu

from services.Tcliente_service import ClienteService
from services.Tpelicula_service import PeliculaService
from services.Treservas_service import ReservaService
from services.Tfuncion_service import FuncionService
from services.Tpromociones_services import PromocionesService

from views.Tabs.cliente_tab import ClientesTab
from views.Tabs.pelicula_tab import PeliculasTab
from views.Tabs.reserva_tab import ReservasTab
from views.Tabs.funcion_tab import FuncionesTab
from views.Tabs.promociones_tab import PromocionesTab

class TrabajadorView(ctk.CTk):
    def __init__(self, employee_name):
        super().__init__()
        self.title("Panel de Trabajador")
        self.geometry("1100x700")

        self.header = HeaderBar(self, employee_name)

        def on_tab_selected(tab_name):
            self.tabview.set(tab_name)

        self.sidebar = SidebarMenu(self, on_tab_selected)
        self.sidebar.pack(side="left", fill="y")

        self.boton_api = ctk.CTkButton(self, text="Ir a API", command=self.abrir_api)
        self.boton_api.place(relx=1.0, rely=1.0, anchor="se")

    def abrir_api(self):
        webbrowser.open("http://localhost:8000/docs")

        # Tabview principal
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Instancia los services con la sesión de base de datos
        self.cliente_service = ClienteService
        self.pelicula_service = PeliculaService
        self.reserva_service = ReservaService
        self.funcion_service = FuncionService
        self.promociones_service = PromocionesService

        # Agrega cada tab correctamente
        self.tabview.add("Clientes")
        self.cliente_tab = ClientesTab(self.tabview.tab("Clientes"), self.cliente_service)

        self.tabview.add("Películas")
        self.pelicula_tab = PeliculasTab(self.tabview.tab("Películas"), self.pelicula_service)

        self.tabview.add("Reservas")
        self.reserva_tab = ReservasTab(self.tabview.tab("Reservas"), self.reserva_service)

        self.tabview.add("Funciones")
        self.funcion_tab = FuncionesTab(self.tabview.tab("Funciones"), self.funcion_service)

        self.tabview.add("Promociones")
        self.promociones_tab = PromocionesTab(self.tabview.tab("Promociones"), self.promociones_service)