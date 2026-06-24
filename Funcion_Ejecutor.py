# ejecutor.py
import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
from base_datos import registrar_operacion # Importamos la función de registro

# Cargamos las variables de entorno
load_dotenv()
API_KEY = os.getenv('ALPACA_API_KEY')
SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
BASE_URL = 'https://paper-api.alpaca.markets'

# Iniciamos el cliente REST
api_rest = tradeapi.rest.REST(API_KEY, SECRET_KEY, base_url=BASE_URL)
print("--- Tradibot Execution Engine | By ReyMD9 ---")

def ejecutar_bracket_order(simbolo, precio_actual, cantidad=1):
    """
    Ejecuta una orden Bracket (Compra + TP + SL) y registra el evento.
    """
    try:
        print(f"📡 Preparando Bracket Order para {simbolo}...")
        
        # Cálculos de riesgo (0.5% abajo, 1% arriba)
        precio_sl = precio_actual * 0.995
        precio_tp = precio_actual * 1.010
        
        # Envío de orden a Alpaca
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
        
        # Registro exitoso en la base de datos
        registrar_operacion(
            simbolo=simbolo, 
            cantidad=cantidad, 
            precio_entrada=precio_actual, 
            tipo='BUY_BRACKET'
        )
        
        print(f"✅ ¡Disparo confirmado! Orden ID: {orden.id}")
        print(f"📈 Take Profit: ${precio_tp:.2f} | 📉 Stop Loss: ${precio_sl:.2f}")
        return True
        
    except Exception as e:
        print(f"❌ Error de API en Alpaca: {e}")
        return False
    except Exception as e:
        print(f"❌ Fallo inesperado al ejecutar la orden: {e}")
        return False

# Prueba rápida si ejecutas este archivo directamente
if __name__ == "__main__":
    # Ejemplo: Simular un trade con SPY a precio mercado
    # Nota: Descomentar solo para pruebas unitarias
    # ejecutar_bracket_order('SPY', 530.00)
    pass