from abc import ABC, abstractmethod

class Command(ABC):
    """
    Interfaz base para el patrón Command en la API.
    Todos los comandos deben implementar el método execute.
    """
    
    @abstractmethod
    def execute(self):
        """
        Ejecuta el comando específico.
        Debe ser implementado por cada comando concreto.
        """
        pass