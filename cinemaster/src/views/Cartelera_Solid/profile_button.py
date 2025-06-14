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
        # Ruta absoluta a la carpeta de imágenes
        images_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images"))
        profile_image_path = os.path.join(images_dir, "perfil.png")
        default_image_path = os.path.join(images_dir, "default.png")
        try:
            if os.path.exists(profile_image_path):
                profile_img = Image.open(profile_image_path)
            else:
                print("Imagen de perfil no encontrada, utilizando la imagen predeterminada.")
                profile_img = Image.open(default_image_path)
        except Exception:
            # Si tampoco existe default.png, crea una imagen vacía
            print("Imagen predeterminada no encontrada, usando imagen gris.")
            profile_img = Image.new("RGB", (35, 35), color="gray")
        profile_img = profile_img.resize((35, 35))
        return ImageTk.PhotoImage(profile_img)

    def redirect_to_profile(self):
        """
        Redirige al usuario a la vista de su perfil cuando hace clic en el botón.
        """
        print(f"Redirigiendo a {self.cliente.nombre}'s perfil")
        # Llamamos a la vista de perfil pasando el cliente
        from views.profile_view import ProfileView  # Importar la vista del perfil
        profile_view = ProfileView(self.cliente)  # Pasamos el cliente logueado
        profile_view.mainloop()  # Iniciar la ventana del perfil