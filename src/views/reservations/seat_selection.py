import customtkinter as ctk

class SeatSelectionView(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(row=0, column=0, padx=20, pady=20)

        self.title_label = ctk.CTkLabel(self, text="Selección de Asientos", font=("Arial", 24))
        self.title_label.grid(row=0, column=0, pady=10)

        self.seat_1_button = ctk.CTkButton(self, text="Asiento 1", command=lambda: self.select_seat(1))
        self.seat_1_button.grid(row=1, column=0, padx=5, pady=5)

        self.seat_2_button = ctk.CTkButton(self, text="Asiento 2", command=lambda: self.select_seat(2))
        self.seat_2_button.grid(row=1, column=1, padx=5, pady=5)


    def select_seat(self, seat_number):
        print(f"Seleccionaste el asiento {seat_number}")

