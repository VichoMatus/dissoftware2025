import customtkinter as ctk
from tkinter import ttk, messagebox

class PeliculasTab(ctk.CTkFrame):
    def __init__(self, parent, pelicula_service):
        super().__init__(parent)
        self.pelicula_service = pelicula_service

        self.label = ctk.CTkLabel(self, text="Lista de Películas", font=("Arial", 20))
        self.label.pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("ID", "Título", "Duración", "Género", "Imagen"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Título", text="Título")
        self.tree.heading("Duración", text="Duración")
        self.tree.heading("Género", text="Género")
        self.tree.heading("Imagen", text="Imagen")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.cargar_datos()

    def cargar_datos(self):
        try:
            peliculas = self.pelicula_service.listar_peliculas()
            for item in self.tree.get_children():
                self.tree.delete(item)
            for pelicula in peliculas:
                self.tree.insert("", "end", values=(
                    pelicula["id_pelicula"],
                    pelicula["Title"],
                    pelicula["Duration"],
                    pelicula["Gender"],
                    pelicula["Image_path"]
                ))
        except Exception as e:
            print(f"Error al cargar películas: {e}")

    def mostrar_formulario_agregar(self):
        top = ctk.CTkToplevel(self)
        top.title("Agregar Película")
        top.geometry("350x350")

        lbl_title = ctk.CTkLabel(top, text="Título:")
        lbl_title.pack(pady=5)
        entry_title = ctk.CTkEntry(top)
        entry_title.pack(pady=5)

        lbl_duration = ctk.CTkLabel(top, text="Duración (min):")
        lbl_duration.pack(pady=5)
        entry_duration = ctk.CTkEntry(top)
        entry_duration.pack(pady=5)

        lbl_gender = ctk.CTkLabel(top, text="Género:")
        lbl_gender.pack(pady=5)
        entry_gender = ctk.CTkEntry(top)
        entry_gender.pack(pady=5)

        lbl_image = ctk.CTkLabel(top, text="Ruta de Imagen:")
        lbl_image.pack(pady=5)
        entry_image = ctk.CTkEntry(top)
        entry_image.pack(pady=5)

        def guardar_pelicula():
            title = entry_title.get()
            duration = entry_duration.get()
            gender = entry_gender.get()
            image_path = entry_image.get()
            if not title or not duration or not image_path:
                messagebox.showerror("Error", "Título, duración e imagen son obligatorios")
                return
            try:
                self.pelicula_service.crear_pelicula(title, int(duration), gender, image_path)
                messagebox.showinfo("Éxito", "Película agregada correctamente")
                top.destroy()
                self.cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar la película:\n{e}")

        btn_guardar = ctk.CTkButton(top, text="Guardar", command=guardar_pelicula, fg_color="#43a047")
        btn_guardar.pack(pady=15)

    def mostrar_formulario_actualizar(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Selecciona una película para actualizar")
            return

        valores = self.tree.item(selected, "values")
        if not valores:
            messagebox.showerror("Error", "No se pudo obtener la información de la película")
            return

        top = ctk.CTkToplevel(self)
        top.title("Actualizar Película")
        top.geometry("350x350")

        lbl_title = ctk.CTkLabel(top, text="Título:")
        lbl_title.pack(pady=5)
        entry_title = ctk.CTkEntry(top)
        entry_title.insert(0, valores[1])
        entry_title.pack(pady=5)

        lbl_duration = ctk.CTkLabel(top, text="Duración (min):")
        lbl_duration.pack(pady=5)
        entry_duration = ctk.CTkEntry(top)
        entry_duration.insert(0, valores[2])
        entry_duration.pack(pady=5)

        lbl_gender = ctk.CTkLabel(top, text="Género:")
        lbl_gender.pack(pady=5)
        entry_gender = ctk.CTkEntry(top)
        entry_gender.insert(0, valores[3])
        entry_gender.pack(pady=5)

        lbl_image = ctk.CTkLabel(top, text="Ruta de Imagen:")
        lbl_image.pack(pady=5)
        entry_image = ctk.CTkEntry(top)
        entry_image.insert(0, valores[4])
        entry_image.pack(pady=5)

        def actualizar_pelicula():
            title = entry_title.get()
            duration = entry_duration.get()
            gender = entry_gender.get()
            image_path = entry_image.get()
            if not title or not duration or not image_path:
                messagebox.showerror("Error", "Título, duración e imagen son obligatorios")
                return
            try:
                self.pelicula_service.actualizar_pelicula(
                    int(valores[0]), title, int(duration), gender, image_path
                )
                messagebox.showinfo("Éxito", "Película actualizada correctamente")
                top.destroy()
                self.cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar la película:\n{e}")

        btn_actualizar = ctk.CTkButton(top, text="Actualizar", command=actualizar_pelicula, fg_color="#fbc02d")
        btn_actualizar.pack(pady=15)

    def eliminar_pelicula_seleccionada(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Selecciona una película para eliminar")
            return

        valores = self.tree.item(selected, "values")
        if not valores:
            messagebox.showerror("Error", "No se pudo obtener la información de la película")
            return

        confirm = messagebox.askyesno("Confirmar", f"¿Seguro que deseas eliminar la película '{valores[1]}'?")
        if not confirm:
            return

        try:
            self.pelicula_service.eliminar_pelicula(int(valores[0]))
            messagebox.showinfo("Éxito", "Película eliminada correctamente")
            self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la película:\n{e}")