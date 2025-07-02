import requests

def confirmar_pago(payload):
    url = "http://127.0.0.1:8000/confirmar_pago/"
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()