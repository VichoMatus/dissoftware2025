import requests
import json
from typing import List, Dict, Optional

class ClienteAPIService:
    """Servicio para interactuar con la API de clientes usando el patrón Prototype para clonado"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000/api"):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}

    def crear_cliente(self, nombre: str, email: str, password: str) -> Optional[Dict]:
        """Crear un nuevo cliente"""
        try:
            data = {
                "nombre": nombre,
                "Email": email,
                "Password": password
            }
            response = requests.post(f"{self.base_url}/clientes/", 
                                   json=data, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error al crear cliente: {e}")
            return None

    def obtener_clientes(self) -> List[Dict]:
        """Obtener todos los clientes"""
        try:
            response = requests.get(f"{self.base_url}/clientes/", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error al obtener clientes: {e}")
            return []

    def obtener_cliente(self, cliente_id: int) -> Optional[Dict]:
        """Obtener un cliente por ID"""
        try:
            response = requests.get(f"{self.base_url}/clientes/{cliente_id}", 
                                  headers=self.headers)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error al obtener cliente: {e}")
            return None

    def actualizar_cliente(self, cliente_id: int, nombre: Optional[str] = None, 
                          email: Optional[str] = None, password: Optional[str] = None) -> Optional[Dict]:
        """Actualizar un cliente"""
        try:
            data = {}
            if nombre: data["nombre"] = nombre
            if email: data["Email"] = email
            if password: data["Password"] = password
            
            response = requests.put(f"{self.base_url}/clientes/{cliente_id}", 
                                  json=data, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error al actualizar cliente: {e}")
            return None

    def eliminar_cliente(self, cliente_id: int) -> bool:
        """Eliminar un cliente"""
        try:
            response = requests.delete(f"{self.base_url}/clientes/{cliente_id}", 
                                     headers=self.headers)
            return response.status_code == 200
        except Exception as e:
            print(f"Error al eliminar cliente: {e}")
            return False

    def clonar_cliente(self, cliente_id: int, nuevo_nombre: str, 
                      nuevo_email: str, nuevo_password: str) -> Optional[Dict]:
        """Clonar un cliente usando el patrón Prototype via API"""
        try:
            data = {
                "nombre": nuevo_nombre,
                "Email": nuevo_email,
                "Password": nuevo_password
            }
            response = requests.post(f"{self.base_url}/clientes/{cliente_id}/clone", 
                                   json=data, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error al clonar cliente: {e}")
            return None
