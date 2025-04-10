import sys
import os
import customtkinter as ctk
import tkinter.messagebox as tkmb

# Añadir el directorio 'src' al sys.path para permitir el acceso a 'views'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src')))

class SeatSelection(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(row=0, column=0, sticky="nsew")
        
        self.create_widgets()

        # Inicializamos on_seat_selection_complete
        self.on_seat_selection_complete = None

    def create_widgets(self):
        # Título
        self.title_label = ctk.CTkLabel(self, text="¡Selecciona tu Asiento!", font=("Arial", 24, "bold"))
        self.title_label.grid(row=0, column=0, pady=20)

        # Etiqueta de selección de asiento
        self.label = ctk.CTkLabel(self, text="Seleccione un asiento:", font=("Arial", 14))
        self.label.grid(row=1, column=0, pady=10)

        # Lista de asientos disponibles (simulamos 10 asientos)
        self.seats = [f"Asiento {i}" for i in range(1, 11)]
        self.seat_var = ctk.StringVar(value=self.seats[0])  # Valor predeterminado

        # Dropdown para seleccionar el asiento
        self.seat_dropdown = ctk.CTkOptionMenu(self, variable=self.seat_var, values=self.seats)
        self.seat_dropdown.grid(row=2, column=0, pady=20)

        # Botón para confirmar la selección de asiento
        self.select_button = ctk.CTkButton(self, text="Reservar Asiento", command=self.confirm_seat, 
                                           font=("Arial", 16), fg_color="#4CAF50", hover_color="#45a049", width=200)
        self.select_button.grid(row=3, column=0, pady=20)

        # Ajustar el diseño para que ocupe todo el espacio disponible
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def confirm_seat(self):
        selected_seat = self.seat_var.get()

        if selected_seat:  # Si el usuario seleccionó un asiento
            # Mostrar mensaje de éxito
            tkmb.showinfo("Éxito", f"El asiento {selected_seat} ha sido reservado con éxito.")
            
            # Llamar a la función de MainView para habilitar el botón de reservas
            if self.on_seat_selection_complete:
                self.on_seat_selection_complete()  # Llamar a la función de habilitación del botón en MainView

            # Volver a la vista principal después de la reserva
            self.show_main_view()  # Volver a mostrar la MainView
            self.grid_forget()  # Ocultar la vista de selección de asiento

        else:
            # Si no se selecciona un asiento
            tkmb.showwarning("Advertencia", "Por favor selecciona un asiento.")

    def show_main_view(self):
        # Importación de MainView aquí para evitar importación circular
        from views.main_view import MainView  # La importación ahora se realiza correctamente

        # Verificar si el widget sigue existiendo antes de ejecutar cualquier operación
        if self.winfo_exists():  # Verificar si el widget sigue existiendo
            self.master.destroy()  # Destruir la vista actual (SeatSelection)
            new_main_view = MainView()  # Crear la nueva instancia de MainView
            new_main_view.mainloop()  # Iniciar el ciclo de eventos de la MainView
        else:
            print("La ventana ya ha sido destruida o no existe.")
