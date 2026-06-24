import sqlite3
import pandas as pd

def obtener_reporte_rendimiento(fecha_inicio, fecha_fin):
    # Conectamos a la base de datos
    conn = sqlite3.connect("trade_history.db")
    
    # Leemos los datos en un DataFrame de pandas para procesarlos fácilmente
    query = f"SELECT * FROM trades WHERE fecha BETWEEN '{fecha_inicio}' AND '{fecha_fin}'"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if df.empty:
        return "No hay operaciones en este rango de tiempo."
    
    # Ejemplo de cálculos básicos
    total_trades = len(df)
    simbolos_operados = df['simbolo'].unique()
    
    reporte = {
        "Total de Trades": total_trades,
        "Acciones": list(simbolos_operados),
        "Detalle": df
    }
    return reporte

# Prueba rápida
if __name__ == "__main__":
    # Cambia las fechas por pruebas
    print(obtener_reporte_rendimiento("2026-01-01", "2026-12-31"))