from .command import Command
from typing import List, Dict, Any

class CommandInvoker:
    """
    Invocador de comandos para la API.
    Permite ejecutar comandos individuales o en lote.
    """
    
    def __init__(self):
        self.commands: List[Command] = []
        self.results: List[Dict[str, Any]] = []
    
    def add_command(self, command: Command):
        """Agrega un comando a la lista de comandos a ejecutar"""
        self.commands.append(command)
    
    def execute_commands(self) -> List[Dict[str, Any]]:
        """
        Ejecuta todos los comandos en orden y recopila los resultados.
        
        Returns:
            Lista con los resultados de cada comando ejecutado
        """
        self.results.clear()
        
        for i, command in enumerate(self.commands):
            try:
                print(f"🔄 Ejecutando comando {i+1}/{len(self.commands)}: {command.__class__.__name__}")
                result = command.execute()
                self.results.append(result)
                
                # Si algún comando falla, podríamos decidir si continuar o parar
                if not result.get("success", False):
                    print(f"⚠️ Comando {command.__class__.__name__} falló: {result.get('message', 'Error desconocido')}")
                
            except Exception as e:
                error_result = {
                    "success": False,
                    "command": command.__class__.__name__,
                    "error": str(e)
                }
                self.results.append(error_result)
                print(f"❌ Error ejecutando {command.__class__.__name__}: {e}")
        
        return self.results
    
    def execute_single_command(self, command: Command) -> Dict[str, Any]:
        """
        Ejecuta un solo comando y devuelve su resultado.
        
        Args:
            command: Comando a ejecutar
            
        Returns:
            Resultado de la ejecución del comando
        """
        try:
            print(f"🔄 Ejecutando comando único: {command.__class__.__name__}")
            result = command.execute()
            return result
        except Exception as e:
            print(f"❌ Error ejecutando {command.__class__.__name__}: {e}")
            return {
                "success": False,
                "command": command.__class__.__name__,
                "error": str(e)
            }
    
    def clear_commands(self):
        """Limpia la lista de comandos"""
        self.commands.clear()
        self.results.clear()