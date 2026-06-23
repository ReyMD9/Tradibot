import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('ALPACA_API_KEY')
SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')

if not API_KEY:
    print("⚠️ ALERTA: No se cargó la API_KEY. Revisa tu archivo .env")
else:
    print(f"🔑 Llave detectada: {API_KEY[:4]}... cargada en memoria.")

url_datos = "https://data.alpaca.markets/v2/stocks/SPY/trades/latest?feed=iex"

headers = {
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": SECRET_KEY
}

print("📡 Consultando el precio en el servidor de Alpaca (Flujo IEX)...")
respuesta = requests.get(url_datos, headers=headers)

if respuesta.status_code == 200:
    datos = respuesta.json()
    precio = datos['trade']['p']
    hora_utc = datos['trade']['t']
    
    print("Conexión exitosa!")
    print(f"Último precio de SPY: ${precio}")
    print(f"⏱ Marca de tiempo (UTC): {hora_utc}")
else:
    print(f"❌ Error en la matriz. Código {respuesta.status_code}: {respuesta.text}")