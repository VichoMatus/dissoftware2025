from abc import ABC, abstractmethod
from typing import Dict, Any

class Observer(ABC):
    """
    Interfaz base para el patrón Observer en la API.
    Los observadores reciben notificaciones cuando ocurren eventos.
    """
    
    @abstractmethod
    def update(self, event_data: Dict[str, Any]):
        """
        Método llamado cuando ocurre un evento.
        
        Args:
            event_data: Diccionario con los datos del evento
        """
        pass

class Subject(ABC):
    """
    Interfaz base para sujetos observables en la API.
    Mantiene una lista de observadores y les notifica cuando hay cambios.
    """
    
    def __init__(self):
        self._observers = []
    
    def attach(self, observer: Observer):
        """Agrega un observador a la lista"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer):
        """Remueve un observador de la lista"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event_data: Dict[str, Any]):
        """Notifica a todos los observadores sobre un evento"""
        for observer in self._observers:
            try:
                observer.update(event_data)
            except Exception as e:
                print(f"❌ Error notificando observador {observer.__class__.__name__}: {e}")