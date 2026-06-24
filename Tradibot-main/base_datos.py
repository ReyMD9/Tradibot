import sqlite3
from datetime import datetime

# Conexión a la base de datos (se creará el archivo si no existe)
DB_NAME = "trade_history.db"

def inicializar_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TIMESTAMP,
            simbolo TEXT,
            cantidad REAL,
            precio_entrada REAL,
            tipo TEXT
        )
    ''')
    conn.commit()
    conn.close()

def registrar_operacion(simbolo, cantidad, precio_entrada, tipo="COMPRA"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO trades (fecha, simbolo, cantidad, precio_entrada, tipo)
        VALUES (?, ?, ?, ?, ?)
    ''', (datetime.now(), simbolo, cantidad, precio_entrada, tipo))
    conn.commit()
    conn.close()
    print(f"✅ Trade de {simbolo} registrado en la base de datos.")

# Inicializamos la base de datos al importar el módulo
inicializar_db()