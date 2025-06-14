import customtkinter as ctk

class ShowtimeSelectorWidget:
    def __init__(self, parent, showtimes_with_ids):
        self.label = ctk.CTkLabel(parent, text="Horarios disponibles:")
        self.showtimes_strings = [f"{showtime[1].strftime('%Y-%m-%d %H:%M')} - ID: {showtime[0]}" for showtime in showtimes_with_ids]
        self.selected_showtime = ctk.StringVar(value=self.showtimes_strings[0])
        self.dropdown = ctk.CTkOptionMenu(parent, variable=self.selected_showtime, values=self.showtimes_strings)

    def grid(self, row, column, **kwargs):
        self.label.grid(row=row, column=column, sticky="w", **kwargs)
        self.dropdown.grid(row=row+1, column=column, sticky="w", **kwargs)