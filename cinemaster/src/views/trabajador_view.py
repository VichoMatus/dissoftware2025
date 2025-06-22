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
        self.header.pack(fill="x")

        self.cliente_service = ClienteService()
        self.pelicula_service = PeliculaService()
        self.reserva_service = ReservaService()
        self.funcion_service = FuncionService()
        self.promociones_service = PromocionesService()

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.tabview.add("Clientes")
        self.cliente_tab = ClientesTab(self.tabview.tab("Clientes"), self.cliente_service)
        self.cliente_tab.pack(fill="both", expand=True)

        self.tabview.add("Películas")
        self.pelicula_tab = PeliculasTab(self.tabview.tab("Películas"), self.pelicula_service)
        self.pelicula_tab.pack(fill="both", expand=True)

        self.tabview.add("Reservas")
        self.reserva_tab = ReservasTab(self.tabview.tab("Reservas"), self.reserva_service)
        self.reserva_tab.pack(fill="both", expand=True)

        self.tabview.add("Funciones")
        self.funcion_tab = FuncionesTab(self.tabview.tab("Funciones"), self.funcion_service)
        self.funcion_tab.pack(fill="both", expand=True)

        self.tabview.add("Promociones")
        self.promociones_tab = PromocionesTab(self.tabview.tab("Promociones"), self.promociones_service)
        self.promociones_tab.pack(fill="both", expand=True)

        def on_tab_selected(tab_name):
            self.tabview.set(tab_name)
            if tab_name == "Clientes":
                self.cliente_tab.cargar_datos()
            elif tab_name == "Películas":
                self.pelicula_tab.cargar_datos()
            elif tab_name == "Reservas":
                self.reserva_tab.cargar_datos()
            elif tab_name == "Funciones":
                self.funcion_tab.cargar_datos()
            elif tab_name == "Promociones":
                self.promociones_tab.cargar_datos()

        self.sidebar = SidebarMenu(self, on_tab_selected)
        self.sidebar.pack(side="left", fill="y")

        #Boton para abrir la API
        self.boton_api = ctk.CTkButton(self,text="Ir a API",command=self.abrir_api,fg_color="#8e24aa",hover_color="#6d1b7b")
        self.boton_api.place(relx=0.98, rely=0.98, anchor="se")

        self.cliente_tab.cargar_datos()

    def abrir_api(self):
        webbrowser.open("http://localhost:8000/docs")