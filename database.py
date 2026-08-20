import sqlite3
from datetime import datetime

DB_NAME = "telemetria.db"

def inicializar_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Agregamos la columna 'online' (1 para conectado, 0 para error)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lecturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            bpm REAL,
            spo2 REAL,
            temperatura REAL,
            ecg_adc INTEGER,
            ecg_voltaje REAL,
            online INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def guardar_lectura(bpm, spo2, temp, ecg_adc, ecg_v, online_status):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO lecturas (timestamp, bpm, spo2, temperatura, ecg_adc, ecg_voltaje, online)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (datetime.now(), bpm, spo2, temp, ecg_adc, ecg_v, 1 if online_status else 0))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error al guardar en DB: {e}")
