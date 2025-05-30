import time
import functools

def medir_tiempo(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        fin = time.perf_counter()
        duracion = fin - inicio
        print(f"[MEDICIÓN] {func.__name__} tardó {duracion:.4f} segundos.")
        return resultado
    return wrapper