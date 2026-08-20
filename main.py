# -*- coding: utf-8 -*-
"""
Main del sistema de telemetría - Versión con Autodiagnóstico
Supervisa: MAX30100, NTC (MCP3008 Ch0) y ECG (MCP3008 Ch1)
"""

import signal
import sys
import time

# Importar interfaces de sensores
from max30100 import leer_max30100
from temperatura import leer_temperatura
from electrocardiograma import leer_ecg, apagar_spi as apagar_spi_ecg

# Estado compartido y Base de Datos
from database import inicializar_db, guardar_lectura


# ===============================
# MANEJO DE SALIDA LIMPIA
# ===============================
def salir_limpio(sig, frame):
    print("\n\nCerrando sistema de telemetría...")
    try:
        apagar_spi_ecg() # Liberar bus SPI
    except:
        pass
    print("Hardware liberado correctamente. Adiós.")
    sys.exit(0)


# ===============================
# MAIN
# ===============================
# ... (mismos imports y funciones de salida)

def main():
    inicializar_db()
    ultimo_guardado = time.time()

    while True:
        try:
            bpm, spo2, ir = leer_max30100()
            temp_c = leer_temperatura()
            adc, volt, volt_f = leer_ecg()

            sensores_ok = True
            if ir == 0 and (temp_c == 0.0 or temp_c is None):
                sensores_ok = False

            # Actualizamos la RAM local (para el print de esta terminal)
            actualizar({"sensores_online": sensores_ok, "bpm": bpm, "spo2": spo2})

            # GUARDADO EN DB: Ahora incluimos el estado online
            tiempo_ahora = time.time()
            if tiempo_ahora - ultimo_guardado >= 1.0:
                # IMPORTANTE: Guardamos siempre para que la API sepa el estado actual
                guardar_lectura(bpm, spo2, temp_c, adc, volt_f, sensores_ok)
                ultimo_guardado = tiempo_ahora

            if sensores_ok:
                print(f"\rBPM: {bpm:5} | T: {temp_c:5.2f} C", end="", flush=True)
            else:
                print("\r⚠️ SENSORES DESCONECTADOS", end="", flush=True)

        except Exception as e:
            actualizar({"sensores_online": False})
            
        time.sleep(0.02)


# ===============================
# EJECUCIÓN
# ===============================
if __name__ == "__main__":
    signal.signal(signal.SIGINT, salir_limpio)
    main()
