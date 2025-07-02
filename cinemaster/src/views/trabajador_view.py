import customtkinter as ctk
import webbrowser
from tkinter import messagebox

from views.components.header_bar import HeaderBar
from views.components.side_bar_menu import SidebarMenu

from services.Tcliente_service import ClienteAPIService
from services.Tpelicula_service import PeliculaAPIService
from services.Treservas_service import ReservaAPIService
from services.Tfuncion_service import FuncionAPIService

# Importar servicios para clonado
from api.services.admin_cliente_service import ClienteAPIService as AdminClienteService

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
        
        # Servicio adicional para clonado
        self.admin_cliente_service = AdminClienteService()

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

        self.btn_clonar_cliente = ctk.CTkButton(
            self.cliente_btn_frame,
            text="Clonar Cliente",
            command=self.clonar_cliente_seleccionado,
            fg_color="#9c27b0"
        )
        self.btn_clonar_cliente.pack(side="left", padx=5, pady=5)

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

    def clonar_cliente_seleccionado(self):
        """Clonar un cliente seleccionado usando el patrón Prototype via API"""
        try:
            # Obtener cliente seleccionado del tab
            selected_data = self.cliente_tab.get_selected_cliente_data()
            if not selected_data:
                messagebox.showwarning("Advertencia", "Por favor seleccione un cliente para clonar.")
                return
            
            cliente_id = selected_data.get('id')
            if not cliente_id:
                messagebox.showerror("Error", "No se pudo obtener el ID del cliente seleccionado.")
                return
            
            # Obtener datos del cliente original
            cliente_original = self.admin_cliente_service.obtener_cliente(cliente_id)
            if not cliente_original:
                messagebox.showerror("Error", f"No se encontró cliente con ID {cliente_id}.")
                return
            
            # Crear diálogo para nuevos datos
            dialog = ctk.CTkToplevel(self)
            dialog.title("Clonar Cliente - Nuevos Datos")
            dialog.geometry("400x300")
            dialog.transient(self)
            dialog.grab_set()
            
            ctk.CTkLabel(dialog, text=f"Clonando: {cliente_original['nombre']}", font=("Arial", 14, "bold")).pack(pady=10)
            ctk.CTkLabel(dialog, text="Ingrese los nuevos datos:", font=("Arial", 12)).pack(pady=5)
            
            # Campos para nuevos datos
            ctk.CTkLabel(dialog, text="Nuevo Nombre:").pack(pady=5)
            entry_nuevo_nombre = ctk.CTkEntry(dialog, width=300)
            entry_nuevo_nombre.pack(pady=5)
            entry_nuevo_nombre.insert(0, cliente_original['nombre'] + "_clone")
            
            ctk.CTkLabel(dialog, text="Nuevo Email:").pack(pady=5)
            entry_nuevo_email = ctk.CTkEntry(dialog, width=300)
            entry_nuevo_email.pack(pady=5)
            
            ctk.CTkLabel(dialog, text="Nueva Contraseña:").pack(pady=5)
            entry_nueva_password = ctk.CTkEntry(dialog, width=300, show="*")
            entry_nueva_password.pack(pady=5)
            
            def ejecutar_clonado():
                nuevo_nombre = entry_nuevo_nombre.get()
                nuevo_email = entry_nuevo_email.get()
                nueva_password = entry_nueva_password.get()
                
                if not (nuevo_nombre and nuevo_email and nueva_password):
                    messagebox.showerror("Error", "Todos los campos son obligatorios")
                    return
                
                # Usar el patrón Prototype via API
                resultado = self.admin_cliente_service.clonar_cliente(cliente_id, nuevo_nombre, nuevo_email, nueva_password)
                if resultado:
                    messagebox.showinfo("Éxito", f"Cliente clonado exitosamente con ID {resultado['cliente_id']}.")
                    # Refrescar la lista de clientes
                    self.cliente_tab.cargar_datos()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Error al clonar cliente. Verifique que el email no exista.")
            
            def cancelar():
                dialog.destroy()
            
            # Botones
            btn_frame = ctk.CTkFrame(dialog)
            btn_frame.pack(pady=20)
            
            ctk.CTkButton(btn_frame, text="Clonar", command=ejecutar_clonado).pack(side="left", padx=10)
            ctk.CTkButton(btn_frame, text="Cancelar", command=cancelar).pack(side="left", padx=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al clonar cliente: {str(e)}")
            print(f"Error en clonar_cliente_seleccionado: {e}")

