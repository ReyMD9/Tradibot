# momentum_motor.py
import os
import asyncio
import threading
import schedule
import time
from generador_reporte import generar_pdf_auditoria
from collections import deque
from dotenv import load_dotenv
from alpaca_trade_api.stream import Stream

# IMPORTAMOS TU NUEVO MÓDULO (La magia de la modularidad)
from Funcion_Ejecutor import ejecutar_bracket_order 

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
            
            # >>> EL DISPARO REAL <<<
            # Llamamos a la función que trajimos del otro archivo
            ejecutar_bracket_order(simbolo, precio_actual)
            
            print("="*50)

# --- Tarea de reporte automático ---
def tarea_reporte():
    print("🕒 Generando reporte automático de auditoría...")
    generar_pdf_auditoria("reporte_automatico.pdf")

# --- Hilo para el scheduler ---
def correr_programador():
    # Programa el reporte, por ejemplo, cada 24 horas o cada hora
    schedule.every().day.at("16:00").do(tarea_reporte) 
    
    while True:
        schedule.run_pending()
        time.sleep(60)

# --- 3. Ejecución Principal ---
def iniciar_radar():
    # Reporte inicial al arrancar
    print("🚀 Bot iniciado: Generando auditoría de inicio...")
    generar_pdf_auditoria("reporte_inicio.pdf")
    
    # Iniciar el hilo del reporte en background
    hilo_reporte = threading.Thread(target=correr_programador, daemon=True)
    hilo_reporte.start()
    
    print("📡 Radar activo. Esperando datos...")
    conn.subscribe_bars(analizar_mercado, 'SPY', 'AAPL')
    try:
        conn.run()
    except KeyboardInterrupt:
        print("\nRadar apagado.")

if __name__ == "__main__":
    iniciar_radar()