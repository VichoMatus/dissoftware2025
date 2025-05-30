import sqlite3

# Conectar a la base de datos (asegúrate de usar el nombre correcto del archivo de base de datos)
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# Ejecutar la consulta SQL para insertar un nuevo administrador
cursor.execute("""
INSERT INTO Administrador (nombre, Email, Password) 
VALUES (?, ?, ?)
""", ('Administrador', 'cinemaster@gmail.com', 'cinemaster2025'))

# Confirmar los cambios
conn.commit()

# Cerrar la conexión
conn.close()
