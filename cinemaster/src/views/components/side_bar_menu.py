import customtkinter as ctk

class SidebarMenu(ctk.CTkFrame):
    def __init__(self, parent, on_tab_selected):
        super().__init__(parent, width=150)

        self.buttons = {
            "Clientes": lambda: on_tab_selected("Clientes"),
            "Películas": lambda: on_tab_selected("Peliculas"),
            "Funciones": lambda: on_tab_selected("Funciones"),
            "Reservas": lambda: on_tab_selected("Reservas"),
            "Promociones": lambda: on_tab_selected("Promociones"),
        }

        for text, command in self.buttons.items():
            ctk.CTkButton(self, text=text, command=command).pack(pady=10, padx=10, fill="x")