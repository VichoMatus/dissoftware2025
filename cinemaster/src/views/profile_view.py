import customtkinter as ctk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import requests  # Para hacer las llamadas a la API
import json

# URL base de la API. Centralizada para fácil mantenimiento.
API_BASE_URL = "http://127.0.0.1:8000/profile"

class ProfileView(ctk.CTk):
    def __init__(self, cliente_obj):
        super().__init__()
        self.title("Perfil del Cliente")
        self.geometry("1280x720")

        # Guardamos solo la información necesaria. El ID es clave.
        self.cliente_id = cliente_obj.cliente_id
        self.cliente_nombre = cliente_obj.nombre
        self.cliente_email = cliente_obj.Email # Asumiendo que el objeto tiene este atributo

        self.crear_ui()
        self.mostrar_actualizar_datos() # Mostrar la primera pantalla por defecto

    def crear_ui(self):
        # ... El código para crear la UI no cambia ...
        self.frame_header = ctk.CTkFrame(self, height=60)
        self.frame_header.pack(side="top", fill="x", padx=10, pady=10)
        try:
            current_dir = os.path.dirname(__file__)
            logo_path = os.path.join(current_dir, "images", "logo.png")
            self.logo_image = Image.open(logo_path)
            self.logo_image = self.logo_image.resize((50, 50))
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
            logo_label = ctk.CTkLabel(self.frame_header, image=self.logo_photo, text="")
        except Exception:
            logo_label = ctk.CTkLabel(self.frame_header, text="[Logo]")
        logo_label.pack(side="left", padx=10)
        ctk.CTkLabel(self.frame_header, text="CineMaster", font=("Arial", 20, "bold")).pack(side="left", padx=10)
        self.header_title = ctk.CTkLabel(self.frame_header, text=f"Bienvenido, {self.cliente_nombre}", font=("Arial", 20, "bold"))
        self.header_title.pack(side="right", padx=10)
        self.frame_body = ctk.CTkFrame(self)
        self.frame_body.pack(fill="both", expand=True, padx=10, pady=10)
        self.frame_left = ctk.CTkFrame(self.frame_body, width=200)
        self.frame_left.pack(side="left", fill="y", padx=10, pady=10)
        ctk.CTkButton(self.frame_left, text="Actualizar Datos", command=self.mostrar_actualizar_datos).pack(pady=10)
        ctk.CTkButton(self.frame_left, text="Ver Reservas Actuales", command=self.mostrar_reservas_actuales).pack(pady=10)
        ctk.CTkButton(self.frame_left, text="Ver Historial de Reservas", command=self.mostrar_historial_reservas).pack(pady=10)
        self.frame_right = ctk.CTkFrame(self.frame_body)
        self.frame_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def _limpiar_frame_derecho(self, titulo):
        """Limpia el frame derecho y pone un título nuevo."""
        for widget in self.frame_right.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.frame_right, text=titulo, font=("Arial", 18)).pack(pady=10)

    def mostrar_actualizar_datos(self):
        self._limpiar_frame_derecho("Actualizar Datos")
        self.nombre_entry = ctk.CTkEntry(self.frame_right, width=250)
        self.nombre_entry.insert(0, self.cliente_nombre)
        self.nombre_entry.pack(pady=5)
        self.email_entry = ctk.CTkEntry(self.frame_right, width=250)
        self.email_entry.insert(0, self.cliente_email)
        self.email_entry.pack(pady=5)
        self.contraseña_entry = ctk.CTkEntry(self.frame_right, placeholder_text="Nueva contraseña (dejar en blanco para no cambiar)", show="*", width=250)
        self.contraseña_entry.pack(pady=5)
        ctk.CTkButton(self.frame_right, text="Actualizar", command=self.actualizar_datos).pack(pady=10)

    def actualizar_datos(self):
        # --- Lógica movida a la API ---
        url = f"{API_BASE_URL}/update/{self.cliente_id}"
        payload = {
            "nombre": self.nombre_entry.get(),
            "email": self.email_entry.get(),
            "password": self.contraseña_entry.get() or "dummy_password_to_pass_validation" # O manejar esto en la API
        }
        try:
            response = requests.put(url, json=payload)
            if response.status_code == 200:
                self.cliente_nombre = payload["nombre"]
                self.header_title.configure(text=f"Bienvenido, {self.cliente_nombre}")
                messagebox.showinfo("Éxito", "Datos actualizados correctamente")
            else:
                messagebox.showerror("Error de API", response.json().get("detail", "Error desconocido"))
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la API: {e}")

    def _cargar_reservas(self, es_historial):
        """Función genérica para cargar reservas actuales o del historial desde la API."""
        url = f"{API_BASE_URL}/{self.cliente_id}/reservations"
        params = {"historical": es_historial}
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                messagebox.showerror("Error de API", response.json().get("detail", "Error al cargar reservas"))
                return []
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la API: {e}")
            return []

    def _crear_y_poblar_treeview(self, frame, data):
        """Crea y llena un Treeview con los datos de las reservas."""
        tree = ttk.Treeview(frame, columns=("ID", "Película", "Fecha", "Asiento"), show="headings")
        for col in ("ID", "Película", "Fecha", "Asiento"):
            tree.heading(col, text=col)
        for item in data:
            tree.insert("", "end", values=(item['reservation_id'], item['pelicula'], item['fecha'], item['asientos']))
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        return tree

    def mostrar_reservas_actuales(self):
        self._limpiar_frame_derecho("Reservas Actuales")
        reservas_data = self._cargar_reservas(es_historial=False)
        if reservas_data is not None:
            self.tree_reservas = self._crear_y_poblar_treeview(self.frame_right, reservas_data)
            ctk.CTkButton(self.frame_right, text="Cancelar Reserva", command=self.cancelar_reserva).pack(pady=10)

    def mostrar_historial_reservas(self):
        self._limpiar_frame_derecho("Historial de Reservas")
        reservas_data = self._cargar_reservas(es_historial=True)
        if reservas_data is not None:
            self._crear_y_poblar_treeview(self.frame_right, reservas_data)

    def cancelar_reserva(self):
        if not hasattr(self, 'tree_reservas') or not self.tree_reservas.selection():
            messagebox.showwarning("Sin selección", "Por favor, selecciona una reserva para cancelar.")
            return
        
        selected_item = self.tree_reservas.selection()[0]
        reserva_id = self.tree_reservas.item(selected_item, "values")[0]

        if not messagebox.askyesno("Confirmar", f"¿Seguro que quieres cancelar la reserva {reserva_id}?"):
            return

        url = f"{API_BASE_URL}/reservations/cancel/{reserva_id}"
        try:
            response = requests.delete(url)
            if response.status_code == 200:
                messagebox.showinfo("Éxito", response.json().get("message"))
                self.mostrar_reservas_actuales() # Recargar la lista
            else:
                messagebox.showerror("Error de API", response.json().get("detail", "Error desconocido"))
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la API: {e}")
