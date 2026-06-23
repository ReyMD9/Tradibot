import requests
import os
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv('ALPACA_API_KEY')
SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')

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