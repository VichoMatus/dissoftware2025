import customtkinter as ctk
from controllers.app_controller import AppController

def main():
    ctk.set_appearance_mode("dark")
    app_controller = AppController()
    app_controller.start()

if __name__ == "__main__":
    main()
