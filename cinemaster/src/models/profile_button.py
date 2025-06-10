import os
from PIL import Image, ImageTk
import customtkinter as ctk

class ProfileButton(ctk.CTkButton):
    def __init__(self, parent, cliente, *args, **kwargs):
        """
        Constructor de la clase ProfileButton.

        :param parent: El contenedor donde el botón será colocado (por ejemplo, el header_frame).
        :param cliente: El objeto cliente con la información del cliente logueado.
        """
        self.cliente = cliente
        self.parent = parent

        # Cargar la imagen de perfil
        profile_img = self.load_profile_image()
        
        # Configurar el texto del botón y la acción
        super().__init__(self.parent, text=self.cliente.nombre, font=("Arial", 14),
                         image=profile_img, compound="left", command=self.redirect_to_profile, *args, **kwargs)
        self.image = profile_img  # Mantener la referencia de la imagen para evitar que se elimine
        self.pack(side="right", padx=10)

    def load_profile_image(self):
        """
        Intenta cargar la imagen de perfil del cliente. Si no se encuentra, carga una imagen predeterminada.
        
        :return: Imagen cargada y redimensionada para el botón.
        """
        try:
            current_dir = os.path.dirname(__file__)  # Directorio actual
            # Usar la carpeta views/images para las imágenes
            profile_image_path = os.path.join(current_dir, "../views/images", "perfil.png")  # Ruta relativa
            profile_img = Image.open(profile_image_path)
            profile_img = profile_img.resize((35, 35))  # Redimensionar la imagen
            return ImageTk.PhotoImage(profile_img)
        except FileNotFoundError:
            print(f"Imagen de perfil no encontrada, utilizando la imagen predeterminada.")
            # Si no se encuentra la imagen de perfil, carga una imagen por defecto
            default_img = Image.open(os.path.join(os.path.dirname(__file__), "../views/images", "default.png"))
            default_img = default_img.resize((35, 35))
            return ImageTk.PhotoImage(default_img)

    def redirect_to_profile(self):
        """
        Redirige al usuario a la vista de su perfil cuando hace clic en el botón.
        """
        print(f"Redirigiendo a {self.cliente.nombre}'s perfil")
        # Llamamos a la vista de perfil pasando el cliente
        from views.profile_view import ProfileView  # Importar la vista del perfil
        profile_view = ProfileView(self.cliente)  # Pasamos el cliente logueado
        profile_view.mainloop()  # Iniciar la ventana del perfil
