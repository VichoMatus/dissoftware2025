import customtkinter as ctk

class NotificationView(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(row=0, column=0, padx=20, pady=20)

        self.title_label = ctk.CTkLabel(self, text="Notificaciones", font=("Arial", 24))
        self.title_label.grid(row=0, column=0, pady=10)

        self.notification_label = ctk.CTkLabel(self, text="No tienes nuevas notificaciones")
        self.notification_label.grid(row=1, column=0, pady=10)

