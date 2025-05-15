import customtkinter as ctk
from tkinter import ttk, messagebox
from models.database import SessionLocal
from models.cliente import Cliente  # Asegúrate de que Cliente tenga los métodos correctos
from tkinter import simpledialog
from PIL import Image, ImageTk  # Para el logo
import os


class ProfileView(ctk.CTk):
    def __init__(self, cliente_obj):
        super().__init__()
        self.title("Perfil del Cliente")
        self.geometry("1280x720")

        self.cliente = cliente_obj
        self.crear_ui()

    def crear_ui(self):
        # Header Frame with logo and title
        self.frame_header = ctk.CTkFrame(self, height=60)
        self.frame_header.pack(side="top", fill="x", padx=10, pady=10)

        # Add logo (assuming logo.png is available)
        try:
            current_dir = os.path.dirname(__file__)
            logo_path = os.path.join(current_dir, "images", "logo.png")
            self.logo_image = Image.open(logo_path)
            self.logo_image = self.logo_image.resize((50, 50))
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
            logo_label = ctk.CTkLabel(self.frame_header, image=self.logo_photo, text="")
        except Exception as e:
            logo_label = ctk.CTkLabel(self.frame_header, text="[Logo]")
        
        logo_label.pack(side="left", padx=10)
        
        # Application name
        ctk.CTkLabel(self.frame_header, text="CineMaster", font=("Arial", 20, "bold")).pack(side="left", padx=10)
        
        # User info (greeting) -> Change 'Nombre' to 'nombre'
        ctk.CTkLabel(self.frame_header, text=f"Bienvenido, {self.cliente.nombre}", font=("Arial", 20, "bold")).pack(side="right", padx=10)

        # Main Body Frame (left and right side)
        self.frame_body = ctk.CTkFrame(self)
        self.frame_body.pack(fill="both", expand=True, padx=10, pady=10)

        # Left Frame with buttons
        self.frame_left = ctk.CTkFrame(self.frame_body, width=200)
        self.frame_left.pack(side="left", fill="y", padx=10, pady=10)

        self.btn_actualizar_datos = ctk.CTkButton(self.frame_left, text="Actualizar Datos", command=self.mostrar_actualizar_datos)
        self.btn_actualizar_datos.pack(pady=10)

        self.btn_ver_reservas = ctk.CTkButton(self.frame_left, text="Ver Reservas Actuales", command=self.mostrar_reservas_actuales)
        self.btn_ver_reservas.pack(pady=10)

        self.btn_ver_historial = ctk.CTkButton(self.frame_left, text="Ver Historial de Reservas", command=self.mostrar_historial_reservas)
        self.btn_ver_historial.pack(pady=10)

        # Right Frame for content (dynamic loading)
        self.frame_right = ctk.CTkFrame(self.frame_body)
        self.frame_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def mostrar_actualizar_datos(self):
        # Clear the right frame and display update form
        for widget in self.frame_right.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.frame_right, text="Actualizar Datos", font=("Arial", 18)).pack(pady=10)

        # Form for updating client info
        self.nombre_entry = ctk.CTkEntry(self.frame_right, placeholder_text="Nombre")
        self.nombre_entry.insert(0, self.cliente.nombre)  # Corrected 'nombre' attribute
        self.nombre_entry.pack(pady=5)

        self.email_entry = ctk.CTkEntry(self.frame_right, placeholder_text="Correo")
        self.email_entry.insert(0, self.cliente.Email)  # Corrected 'Email' attribute
        self.email_entry.pack(pady=5)

        self.contraseña_entry = ctk.CTkEntry(self.frame_right, placeholder_text="Contraseña", show="*")
        self.contraseña_entry.insert(0, self.cliente.Password)  # Corrected 'Password' attribute
        self.contraseña_entry.pack(pady=5)

        self.btn_guardar = ctk.CTkButton(self.frame_right, text="Actualizar", command=self.actualizar_datos)
        self.btn_guardar.pack(pady=10)

    def actualizar_datos(self):
        # Get new data from the entry fields
        nuevo_nombre = self.nombre_entry.get()
        nuevo_email = self.email_entry.get()
        nueva_contraseña = self.contraseña_entry.get()

        # Verificación de que la contraseña tiene al menos 4 caracteres
        if len(nueva_contraseña) < 4:
            messagebox.showerror("Error", "La contraseña debe tener al menos 4 caracteres.")
            return

        # Start a session with the database
        session = SessionLocal()

        try:
            # Fetch the client instance by its ID
            cliente_db = session.query(Cliente).filter(Cliente.cliente_id == self.cliente.cliente_id).first()

            if cliente_db:
                # Update the fields with the new values
                cliente_db.nombre = nuevo_nombre
                cliente_db.Email = nuevo_email
                cliente_db.Password = nueva_contraseña

                # Commit the changes to the database
                session.commit()
                messagebox.showinfo("Éxito", "Datos actualizados correctamente")
            else:
                messagebox.showerror("Error", "Cliente no encontrado en la base de datos")

        except Exception as e:
            session.rollback()  # Rollback in case of error
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
        finally:
            session.close()

    def mostrar_reservas_actuales(self):
        # Clear right frame and show current reservations
        for widget in self.frame_right.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.frame_right, text="Reservas Actuales", font=("Arial", 18)).pack(pady=10)

        # Treeview for showing current reservations
        self.tree_reservas = ttk.Treeview(self.frame_right, columns=("ID", "Película", "Fecha", "Asiento"))
        self.tree_reservas.heading("#1", text="ID")
        self.tree_reservas.heading("#2", text="Película")
        self.tree_reservas.heading("#3", text="Fecha")
        self.tree_reservas.heading("#4", text="Asiento")
        self.tree_reservas.pack(fill="both", expand=True)

        # Populate treeview (example data for now)
        for reserva in self.cliente.obtener_reservas_actuales():  # Ensure this method exists in Cliente model
            self.tree_reservas.insert("", "end", values=reserva)

        self.btn_cancelar_reserva = ctk.CTkButton(self.frame_right, text="Cancelar Reserva", command=self.cancelar_reserva)
        self.btn_cancelar_reserva.pack(pady=10)

    def cancelar_reserva(self):
        # Backend functionality to cancel a reservation
        selected_item = self.tree_reservas.selection()
        if selected_item:
            reserva_id = self.tree_reservas.item(selected_item)["values"][0]
            # Implement logic to cancel reservation in the database here
            messagebox.showinfo("Éxito", f"Reserva {reserva_id} cancelada.")

    def mostrar_historial_reservas(self):
        # Clear right frame and show reservation history
        for widget in self.frame_right.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.frame_right, text="Historial de Reservas", font=("Arial", 18)).pack(pady=10)

        # Treeview for showing past reservations
        self.tree_historial = ttk.Treeview(self.frame_right, columns=("ID", "Película", "Fecha", "Asiento"))
        self.tree_historial.heading("#1", text="ID")
        self.tree_historial.heading("#2", text="Película")
        self.tree_historial.heading("#3", text="Fecha")
        self.tree_historial.heading("#4", text="Asiento")
        self.tree_historial.pack(fill="both", expand=True)

        # Populate treeview with past reservations (example data)
        for reserva in self.cliente.obtener_historial_reservas():  # Ensure this method exists in Cliente model
            self.tree_historial.insert("", "end", values=reserva)
