# ejecutor.py
import os
from dotenv import load_dotenv
from alpaca_trade_api.rest import REST

# Cargamos llaves
load_dotenv()
API_KEY = os.getenv('ALPACA_API_KEY')
SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')

# Iniciamos el cliente REST
api_rest = REST(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets')

def ejecutar_bracket_order(simbolo, precio_actual, cantidad=1):
    try:
        print(f" Preparando Bracket Order para {simbolo}...")
        
        # Matemáticas de riesgo (1% de Take Profit, 0.5% de Stop Loss)
        precio_sl = precio_actual * 0.995
        precio_tp = precio_actual * 1.010
        
        orden = api_rest.submit_order(
            symbol=simbolo,
            qty=cantidad,
            side='buy',
            type='market',
            time_in_force='gtc',
            order_class='bracket',
            take_profit=dict(
                limit_price=round(precio_tp, 2),
            ),
            stop_loss=dict(
                stop_price=round(precio_sl, 2),
                limit_price=round(precio_sl * 0.99, 2),
            )
        )
        print(f" ¡Disparo confirmado! Orden ID: {orden.id}")
        print(f" Take Profit: ${precio_tp:.2f} |  Stop Loss: ${precio_sl:.2f}")
        
    except Exception as e:
        print(f" Fallo al ejecutar la orden: {e}")