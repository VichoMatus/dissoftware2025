import requests
import json
from typing import List, Dict, Optional

class EmpleadoAPIService:
    """Servicio para interactuar con la API de empleados usando el patrón Prototype para clonado"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000/api"):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}

    def crear_empleado(self, name: str, email: str, password: str) -> Optional[Dict]:
        """Crear un nuevo empleado"""
        try:
            data = {
                "Name": name,
                "Email": email,
                "Password": password
            }
            response = requests.post(f"{self.base_url}/empleados/", 
                                   json=data, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error al crear empleado: {e}")
            return None

    def obtener_empleados(self) -> List[Dict]:
        """Obtener todos los empleados"""
        try:
            response = requests.get(f"{self.base_url}/empleados/", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error al obtener empleados: {e}")
            return []

    def obtener_empleado(self, empleado_id: int) -> Optional[Dict]:
        """Obtener un empleado por ID"""
        try:
            response = requests.get(f"{self.base_url}/empleados/{empleado_id}", 
                                  headers=self.headers)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error al obtener empleado: {e}")
            return None

    def actualizar_empleado(self, empleado_id: int, name: Optional[str] = None, 
                           email: Optional[str] = None, password: Optional[str] = None) -> Optional[Dict]:
        """Actualizar un empleado"""
        try:
            data = {}
            if name: data["Name"] = name
            if email: data["Email"] = email
            if password: data["Password"] = password
            
            response = requests.put(f"{self.base_url}/empleados/{empleado_id}", 
                                  json=data, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error al actualizar empleado: {e}")
            return None

    def eliminar_empleado(self, empleado_id: int) -> bool:
        """Eliminar un empleado"""
        try:
            response = requests.delete(f"{self.base_url}/empleados/{empleado_id}", 
                                     headers=self.headers)
            return response.status_code == 200
        except Exception as e:
            print(f"Error al eliminar empleado: {e}")
            return False

    def clonar_empleado(self, empleado_id: int, nuevo_name: str, 
                       nuevo_email: str, nuevo_password: str) -> Optional[Dict]:
        """Clonar un empleado usando el patrón Prototype via API"""
        try:
            data = {
                "Name": nuevo_name,
                "Email": nuevo_email,
                "Password": nuevo_password
            }
            response = requests.post(f"{self.base_url}/empleados/{empleado_id}/clone", 
                                   json=data, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error al clonar empleado: {e}")
            return None
