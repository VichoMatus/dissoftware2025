import customtkinter as ctk
from tkinter import ttk
import tkinter.messagebox as messagebox

class ClientesTab(ctk.CTkFrame):
    def __init__(self, parent, cliente_service):
        super().__init__(parent)
        self.cliente_service = cliente_service

        self.label = ctk.CTkLabel(self, text="Lista de Clientes", font=("Arial", 20))
        self.label.pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("ID", "Nombre", "Correo", "Membresía"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Correo", text="Correo")
        self.tree.heading("Membresía", text="Membresía")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.cargar_datos()

    def cargar_datos(self):
        """Carga los datos de clientes desde el servicio"""
        try:
            clientes = self.cliente_service.listar_clientes()
            self.mostrar_clientes(clientes)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar clientes:\n{e}")

    def mostrar_clientes(self, clientes):
        """Muestra los clientes en el Treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for cliente in clientes:
            self.tree.insert("", "end", values=(
                cliente.get("cliente_id", ""),
                cliente.get("nombre", ""),
                cliente.get("Email", ""),
                "Sí" if cliente.get("Membership", False) else "No"
            ))

    def obtener_cliente_seleccionado(self):
        """Obtiene el cliente seleccionado en el Treeview"""
        selected = self.tree.selection()
        if not selected:
            return None
        values = self.tree.item(selected[0], "values")
        return {
            "cliente_id": values[0],
            "nombre": values[1],
            "email": values[2],
            "membership": values[3] == "Sí"
        }

    def get_selected_cliente_data(self):
        """Obtiene los datos del cliente seleccionado para clonado"""
        selected = self.tree.selection()
        if not selected:
            return None
        values = self.tree.item(selected[0], "values")
        if not values:
            return None
        return {
            "id": values[0],
            "nombre": values[1],
            "email": values[2],
            "membership": values[3] == "Sí"
        }

    def mostrar_formulario_agregar(self):
        """Muestra el formulario para agregar un nuevo cliente"""
        top = ctk.CTkToplevel(self)
        top.title("Agregar Cliente")
        top.geometry("1100x700")
        top.transient(self.master)

        lbl_nombre = ctk.CTkLabel(top, text="Nombre:")
        lbl_nombre.pack(pady=5)
        entry_nombre = ctk.CTkEntry(top)
        entry_nombre.pack(pady=5)

        lbl_email = ctk.CTkLabel(top, text="Email:")
        lbl_email.pack(pady=5)
        entry_email = ctk.CTkEntry(top)
        entry_email.pack(pady=5)

        lbl_password = ctk.CTkLabel(top, text="Password:")
        lbl_password.pack(pady=5)
        entry_password = ctk.CTkEntry(top, show="*")
        entry_password.pack(pady=5)

        def guardar_cliente():
            """Guarda el nuevo cliente"""
            nombre = entry_nombre.get()
            email = entry_email.get()
            password = entry_password.get()
            if not nombre or not email or not password:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            try:
                self.cliente_service.crear_cliente(nombre, email, password)
                messagebox.showinfo("Éxito", "Cliente agregado correctamente")
                top.destroy()
                self.cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar el cliente:\n{e}")

        btn_guardar = ctk.CTkButton(top, text="Guardar", command=guardar_cliente, fg_color="#43a047")
        btn_guardar.pack(pady=15)

    def mostrar_formulario_actualizar(self):
        """Muestra el formulario para actualizar un cliente existente"""
        cliente = self.obtener_cliente_seleccionado()
        if not cliente:
            messagebox.showwarning("Aviso", "Selecciona un cliente para actualizar")
            return

        top = ctk.CTkToplevel(self)
        top.title("Actualizar Cliente")
        top.geometry("1100x700")
        top.transient(self.master)
        self.password_modificada = False

        lbl_nombre = ctk.CTkLabel(top, text="Nombre:")
        lbl_nombre.pack(pady=5)
        entry_nombre = ctk.CTkEntry(top)
        entry_nombre.insert(0, cliente["nombre"])
        entry_nombre.pack(pady=5)

        lbl_email = ctk.CTkLabel(top, text="Email:")
        lbl_email.pack(pady=5)
        entry_email = ctk.CTkEntry(top)
        entry_email.insert(0, cliente["email"])
        entry_email.pack(pady=5)

        lbl_password = ctk.CTkLabel(top, text="Contraseña")
        lbl_password.pack(pady=5)
        
        entry_password = ctk.CTkEntry(top, show="*")
        entry_password.pack(pady=5)
        
        def detectar_cambio_password(*args):
            self.password_modificada = bool(entry_password.get())

        entry_password.bind("<KeyRelease>", detectar_cambio_password)

        def guardar_actualizacion():
            """Guarda los cambios del cliente"""
            nombre = entry_nombre.get()
            email = entry_email.get()
            nueva_password = entry_password.get() if self.password_modificada else None
            
            if not nombre or not email:
                messagebox.showerror("Error", "Nombre y email son obligatorios")
                return
                
            try:
                self.cliente_service.actualizar_cliente(
                    cliente_id=cliente["cliente_id"], 
                    nombre=nombre, 
                    email=email, 
                    password=nueva_password
                )
                
                messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
                top.destroy()
                self.cargar_datos()
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar el cliente:\n{e}")

        btn_guardar = ctk.CTkButton(top, text="Guardar", command=guardar_actualizacion, fg_color="#fbc02d")
        btn_guardar.pack(pady=15)


    def eliminar_cliente_seleccionado(self):
        cliente = self.obtener_cliente_seleccionado()
        if not cliente:
            messagebox.showwarning("Aviso", "Selecciona un cliente para eliminar")
            return
        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar cliente {cliente['nombre']}?")
        if not confirm:
            return
        try:
            self.cliente_service.eliminar_cliente(cliente["cliente_id"])
            messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
            self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el cliente:\n{e}")