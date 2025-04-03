import customtkinter as ctk

class ReservationView(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(row=0, column=0, padx=20, pady=20)

        self.title_label = ctk.CTkLabel(self, text="Reservas", font=("Arial", 24))
        self.title_label.grid(row=0, column=0, pady=10)

        self.select_movie_button = ctk.CTkButton(self, text="Seleccionar Película", command=self.select_movie)
        self.select_movie_button.grid(row=1, column=0, pady=10)

        self.view_reservations_button = ctk.CTkButton(self, text="Ver Mis Reservas", command=self.view_reservations)
        self.view_reservations_button.grid(row=2, column=0, pady=10)

    def select_movie(self):
        print("Seleccionando película...")

    def view_reservations(self):
        print("Mostrando mis reservas...")

