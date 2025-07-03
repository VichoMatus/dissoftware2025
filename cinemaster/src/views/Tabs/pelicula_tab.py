import customtkinter as ctk
import os, datetime, shutil
from PIL import Image
from tkinter import ttk, messagebox, filedialog

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
        top.geometry("1100x700")
        
        top.transient(self.master) 
        self.ruta_imagen_guardada = None
        
        # Campos del formulario
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
        
        # Label para la previsualización de la imagen
        self.label_preview = ctk.CTkLabel(top, text="Previsualización de imagen")
        self.label_preview.pack(pady=10)
        
        # Botón para seleccionar imagen
        btn_seleccionar_imagen = ctk.CTkButton(
            top,
            text="Seleccionar Imagen",
            command=self.seleccionar_imagen
        )
        btn_seleccionar_imagen.pack(pady=10)
        
        btn_guardar = ctk.CTkButton(
            top,
            text="Guardar Película",
            command=lambda: self.guardar_pelicula(
                entry_title.get(),
                entry_duration.get(),
                entry_gender.get(),
                self.ruta_imagen_guardada,
                top
            ),
            fg_color="#43a047"
        )
        btn_guardar.pack(pady=15)

    def seleccionar_imagen(self):
        """Abre diálogo para seleccionar imagen y valida la existencia"""
        try:
            ruta_imagen = filedialog.askopenfilename(
                title="Seleccionar imagen",
                filetypes=[
                    ("Imágenes JPEG", "*.jpg *.jpeg"),
                    ("Imágenes PNG", "*.png"),
                    ("Todos los archivos", "*.*")
                ]
            )
            
            if ruta_imagen:
                if os.path.exists(ruta_imagen):
                    self.ruta_imagen_guardada = ruta_imagen
                    self.mostrar_imagen_previa(ruta_imagen, self.label_preview)
                    return ruta_imagen
                else:
                    messagebox.showerror("Error", "El archivo seleccionado no existe")
            return None
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {str(e)}")
            return None

    def guardar_imagen_en_carpeta_peliculas(self, ruta_origen):
        """Guarda la imagen en la carpeta de imágenes del proyecto"""
        try:
            # Obtiene el directorio base del proyecto
            directorio_base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            carpeta_imagenes = os.path.join(directorio_base, "assets", "imagenes_peliculas")
            
            # Crea la carpeta si no existe
            os.makedirs(carpeta_imagenes, exist_ok=True)
            
            # Genera un nombre único para la imagen
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            extension = os.path.splitext(ruta_origen)[1]
            nombre_archivo = f"pelicula_{timestamp}{extension}"
            ruta_destino = os.path.join(carpeta_imagenes, nombre_archivo)
            
            # Copia la imagen al destino
            shutil.copy2(ruta_origen, ruta_destino)
            
            return ruta_destino
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la imagen: {str(e)}")
            return None

    def mostrar_imagen_previa(self, ruta_imagen, label_widget):
        """Muestra una vista previa de la imagen con manejo robusto de errores"""
        try:
            # Verifica si la ruta existe y es un archivo válido
            if not ruta_imagen or not os.path.isfile(ruta_imagen):
                raise FileNotFoundError("La ruta de la imagen no es válida")
            
            # Usa un context manager para asegurar que el archivo se cierre correctamente
            with Image.open(ruta_imagen) as img:
                # Crea la imagen para CustomTkinter
                imagen_tk = ctk.CTkImage(
                    light_image=img,
                    size=(150, 200)  # Tamaño de la vista previa
                )
                
                # Configura el label
                label_widget.configure(image=imagen_tk, text="")
                label_widget.image = imagen_tk  # Mantén la referencia
                
        except Exception as e:
            print(f"Error al mostrar imagen: {str(e)}")
            label_widget.configure(
                image=None,
                text=f"Error al cargar imagen\n{str(e)}",
                text_color="red"
            )

    def guardar_pelicula(self, titulo, duracion, genero, imagen_path, ventana):
        """Guarda una nueva película en la base de datos y cierra la ventana"""
        try:
            # Validación básica de campos obligatorios
            if not titulo or not duracion or not imagen_path:
                messagebox.showerror("Error", "Título, duración e imagen son campos obligatorios")
                return False
            
            # Convertir duración a entero
            try:
                duracion = int(duracion)
            except ValueError:
                messagebox.showerror("Error", "La duración debe ser un número entero")
                return False
            
            # Llamar al servicio para crear la película
            self.pelicula_service.crear_pelicula(
                Title=titulo,
                Duration=duracion,
                Gender=genero,
                Image_path=imagen_path
            )
            
            messagebox.showinfo("Éxito", "Película agregada correctamente")
            ventana.destroy()  # Cierra la ventana de agregar película
            self.cargar_datos()  # Actualizar la lista
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la película:\n{str(e)}")
            return False


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
        top.geometry("1100x700")

        top.transient(self.master)
        self.nueva_imagen = None

        # Campos del formulario
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

        # Previsualización imagen actual
        self.preview_label = ctk.CTkLabel(top, text="Imagen actual:")
        self.preview_label.pack()
        if valores[4]:
            self.mostrar_imagen_previa(valores[4], self.preview_label)

        # Botón para cambiar imagen
        btn_cambiar_imagen = ctk.CTkButton(
            top,
            text="Cambiar Imagen",
            command=self.cambiar_imagen_actualizar
        )
        btn_cambiar_imagen.pack(pady=10)

        def actualizar_pelicula():
            title = entry_title.get()
            duration = entry_duration.get()
            gender = entry_gender.get()
            image_path = self.nueva_imagen if self.nueva_imagen else valores[4]

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

    def cambiar_imagen_actualizar(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png")]
        )
        if ruta:
            self.nueva_imagen = ruta
            self.mostrar_imagen_previa(ruta, self.preview_label)

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