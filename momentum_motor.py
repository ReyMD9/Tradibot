# momentum_motor.py
import os
import asyncio
from collections import deque
from dotenv import load_dotenv
from alpaca_trade_api.stream import Stream

from ejecutor import ejecutar_bracket_order 

load_dotenv()
API_KEY = os.getenv('ALPACA_API_KEY')
SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')

memoria_precio = deque(maxlen=3)
conn = Stream(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets', data_feed='iex')

async def analizar_mercado(barra):
    simbolo = barra.symbol
    precio_actual = barra.close
    volumen_actual = barra.volume
    
    memoria_precio.append({'precio': precio_actual, 'volumen': volumen_actual})
    print(f"[{simbolo}] Precio: ${precio_actual:.2f} | Vol: {volumen_actual}")
    
    if len(memoria_precio) >= 2:
        vela_anterior = memoria_precio[-2]
        vela_actual = memoria_precio[-1]
        
        cambio_precio = ((vela_actual['precio'] - vela_anterior['precio']) / vela_anterior['precio']) * 100
        
        if cambio_precio > -100:
            print("="*50)
            print("¡MOMENTUM ALCISTA DETECTADO!")
            
            # >>> EL DISPARO  <<<
            ejecutar_bracket_order(simbolo, precio_actual)
            
            print("="*50)

def iniciar_radar():
    print("📡 Levantando radar de Momentum (Esperando datos en vivo)...")
    conn.subscribe_bars(analizar_mercado, 'SPY', 'AAPL')
    try:
        conn.run()
    except KeyboardInterrupt:
        print("\nRadar apagado manualmente.")

if __name__ == "__main__":
    iniciar_radar()