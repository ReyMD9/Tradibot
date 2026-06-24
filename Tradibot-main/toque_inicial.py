import requests

# Reemplaza esto con tus llaves reales recién generadas
API_KEY = "PK73MCL5DWUEEIXOSTSNQWCBDL"
SECRET_KEY = "8DVswmrAiGkKgkh1r6hvToGk9BfxNUbGbvRAumVhmF4f"

url = "https://paper-api.alpaca.markets/v2/account"
headers = {
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": SECRET_KEY
}

# El disparo
respuesta = requests.get(url, headers=headers)

print(f"Estado de red: {respuesta.status_code}")
print("Datos recibidos:")
print(respuesta.json())