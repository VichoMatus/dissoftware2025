import sqlite3
import hashlib
import os

# Cambia estos datos para el nuevo administrador
nuevo_nombre = "elias"
nuevo_email = "elias@gmail.com"
nueva_contraseña = "123456"


db_path = r"C:\Users\elias\OneDrive\Documentos\diseño_de_software\dissoftware2025_GLOBAL\dissoftware2025\test.db"

print(f"Intentando conectar a la base de datos en: {db_path}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Insertar nuevo administrador
cursor.execute("""
    INSERT INTO Administrador (nombre, Email, Password) 
    VALUES (?, ?, ?)
""", (nuevo_nombre, nuevo_email, nueva_contraseña))

conn.commit()
conn.close()

print(f"Administrador '{nuevo_nombre}' agregado correctamente.")
