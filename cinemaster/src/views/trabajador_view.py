import customtkinter as ctk
import webbrowser

from views.components.header_bar import HeaderBar
from views.components.side_bar_menu import SidebarMenu

from services.Tcliente_service import ClienteAPIService
from services.Tpelicula_service import PeliculaAPIService
from services.Treservas_service import ReservaAPIService
from services.Tfuncion_service import FuncionAPIService

from views.Tabs.cliente_tab import ClientesTab
from views.Tabs.pelicula_tab import PeliculasTab
from views.Tabs.reserva_tab import ReservasTab
from views.Tabs.funcion_tab import FuncionesTab


class TrabajadorView(ctk.CTk):
    def __init__(self, employee_name):
        super().__init__()
        self.title("Panel de Trabajador")
        self.geometry("1100x700")

        self.header = HeaderBar(self, employee_name)
        self.header.pack(fill="x")

        self.cliente_service = ClienteAPIService()
        self.pelicula_service = PeliculaAPIService()
        self.reserva_service = ReservaAPIService()
        self.funcion_service = FuncionAPIService()

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(side="left", fill="both", expand=True, padx=10, pady=10)

#--------------------------------------------------------------------------------------------------------#
        self.tabview.add("Clientes")
        self.cliente_tab = ClientesTab(self.tabview.tab("Clientes"), self.cliente_service)
        self.cliente_tab.pack(fill="both", expand=True)

        self.cliente_btn_frame = ctk.CTkFrame(self.tabview.tab("Clientes"))
        self.cliente_btn_frame.pack(fill="x", padx=10, pady=5)

        self.btn_agregar_cliente = ctk.CTkButton(
            self.cliente_btn_frame,
            text="Agregar Cliente",
            command=self.cliente_tab.mostrar_formulario_agregar,
            fg_color="#43a047"
        )
        self.btn_agregar_cliente.pack(side="left", padx=5, pady=5)

        self.btn_leer_cliente = ctk.CTkButton(
            self.cliente_btn_frame,
            text="Leer Clientes",
            command=self.cliente_tab.cargar_datos,
            fg_color="#1976d2"
        )
        self.btn_leer_cliente.pack(side="left", padx=5, pady=5)

        self.btn_actualizar_cliente = ctk.CTkButton(
            self.cliente_btn_frame,
            text="Actualizar Cliente",
            command=self.cliente_tab.mostrar_formulario_actualizar,
            fg_color="#fbc02d"
        )
        self.btn_actualizar_cliente.pack(side="left", padx=5, pady=5)

        self.btn_eliminar_cliente = ctk.CTkButton(
            self.cliente_btn_frame,
            text="Eliminar Cliente",
            command=self.cliente_tab.eliminar_cliente_seleccionado,
            fg_color="#e53935"
        )
        self.btn_eliminar_cliente.pack(side="left", padx=5, pady=5)

#--------------------------------------------------------------------------------------------------------#
        self.tabview.add("Películas")
        self.pelicula_tab = PeliculasTab(self.tabview.tab("Películas"), self.pelicula_service)
        self.pelicula_tab.pack(fill="both", expand=True)

        # Botones CRUD para películas
        self.pelicula_btn_frame = ctk.CTkFrame(self.tabview.tab("Películas"))
        self.pelicula_btn_frame.pack(fill="x", padx=10, pady=5)

        self.btn_agregar_pelicula = ctk.CTkButton(
            self.pelicula_btn_frame,
            text="Agregar Película",
            command=self.pelicula_tab.mostrar_formulario_agregar,
            fg_color="#43a047"
        )
        self.btn_agregar_pelicula.pack(side="left", padx=5, pady=5)

        self.btn_leer_pelicula = ctk.CTkButton(
            self.pelicula_btn_frame,
            text="Leer Películas",
            command=self.pelicula_tab.cargar_datos,
            fg_color="#1976d2"
        )
        self.btn_leer_pelicula.pack(side="left", padx=5, pady=5)

        self.btn_actualizar_pelicula = ctk.CTkButton(
            self.pelicula_btn_frame,
            text="Actualizar Película",
            command=self.pelicula_tab.mostrar_formulario_actualizar,
            fg_color="#fbc02d"
        )
        self.btn_actualizar_pelicula.pack(side="left", padx=5, pady=5)

        self.btn_eliminar_pelicula = ctk.CTkButton(
            self.pelicula_btn_frame,
            text="Eliminar Película",
            command=self.pelicula_tab.eliminar_pelicula_seleccionada,
            fg_color="#e53935"
        )
        self.btn_eliminar_pelicula.pack(side="left", padx=5, pady=5)

#--------------------------------------------------------------------------------------------------------#
        self.tabview.add("Reservas")
        self.reserva_tab = ReservasTab(self.tabview.tab("Reservas"), self.reserva_service)
        self.reserva_tab.pack(fill="both", expand=True)

        self.reserva_btn_frame = ctk.CTkFrame(self.tabview.tab("Reservas"))
        self.reserva_btn_frame.pack(fill="x", padx=10, pady=5)

        self.btn_agregar_reserva = ctk.CTkButton(
            self.reserva_btn_frame,
            text="Agregar Reserva",
            command=self.reserva_tab.mostrar_formulario_agregar,
            fg_color="#43a047"
        )
        self.btn_agregar_reserva.pack(side="left", padx=5, pady=5)

        self.btn_leer_reserva = ctk.CTkButton(
            self.reserva_btn_frame,
            text="Leer Reservas",
            command=self.reserva_tab.cargar_datos,
            fg_color="#1976d2"
        )
        self.btn_leer_reserva.pack(side="left", padx=5, pady=5)

        self.btn_actualizar_reserva = ctk.CTkButton(
            self.reserva_btn_frame,
            text="Actualizar Reserva",
            command=self.reserva_tab.mostrar_formulario_actualizar,
            fg_color="#fbc02d"
        )
        self.btn_actualizar_reserva.pack(side="left", padx=5, pady=5)

        self.btn_eliminar_reserva = ctk.CTkButton(
            self.reserva_btn_frame,
            text="Eliminar Reserva",
            command=self.reserva_tab.eliminar_reserva_seleccionada,
            fg_color="#e53935"
        )
        self.btn_eliminar_reserva.pack(side="left", padx=5, pady=5)
#--------------------------------------------------------------------------------------------------------#
        self.tabview.add("Funciones")
        self.funcion_tab = FuncionesTab(self.tabview.tab("Funciones"), self.funcion_service)
        self.funcion_tab.pack(fill="both", expand=True)
                # Botones CRUD para funciones
        self.funcion_btn_frame = ctk.CTkFrame(self.tabview.tab("Funciones"))
        self.funcion_btn_frame.pack(fill="x", padx=10, pady=5)

        self.btn_agregar_funcion = ctk.CTkButton(
            self.funcion_btn_frame,
            text="Agregar Función",
            command=self.funcion_tab.mostrar_formulario_agregar,
            fg_color="#43a047"
        )
        self.btn_agregar_funcion.pack(side="left", padx=5, pady=5)

        self.btn_leer_funcion = ctk.CTkButton(
            self.funcion_btn_frame,
            text="Leer Funciones",
            command=self.funcion_tab.cargar_datos,
            fg_color="#1976d2"
        )
        self.btn_leer_funcion.pack(side="left", padx=5, pady=5)

        self.btn_actualizar_funcion = ctk.CTkButton(
            self.funcion_btn_frame,
            text="Actualizar Función",
            command=self.funcion_tab.mostrar_formulario_actualizar,
            fg_color="#fbc02d"
        )
        self.btn_actualizar_funcion.pack(side="left", padx=5, pady=5)

        self.btn_eliminar_funcion = ctk.CTkButton(
            self.funcion_btn_frame,
            text="Eliminar Función",
            command=self.funcion_tab.eliminar_funcion_seleccionada,
            fg_color="#e53935"
        )
        self.btn_eliminar_funcion.pack(side="left", padx=5, pady=5)
#--------------------------------------------------------------------------------------------------------#


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