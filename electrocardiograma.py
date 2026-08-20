# -*- coding: utf-8 -*-

import spidev
import time
import csv
import collections

# ===============================
# PARAMETROS
# ===============================
CANAL_ADC = 1
VREF = 3.3
VENTANA_FILTRO = 10
DELAY = 0.01
ARCHIVO_CSV = "ecg_datos.csv"

buffer_filtro = collections.deque(maxlen=VENTANA_FILTRO)

# ===============================
# SPI (lazy init)
# ===============================
_spi = None

def _get_spi():
    global _spi
    if _spi is None:
        _spi = spidev.SpiDev()
        _spi.open(0, 0)
        _spi.max_speed_hz = 1350000
    return _spi

def apagar_spi():
    """Cierra SPI de forma segura (usado por main)"""
    global _spi
    try:
        if _spi:
            _spi.close()
            _spi = None
    except:
        pass

# ===============================
# FUNCIONES BASE
# ===============================
def leer_adc(canal):
    spi = _get_spi()
    r = spi.xfer2([1, (8 + canal) << 4, 0])
    return ((r[1] & 3) << 8) + r[2]

def adc_a_voltaje(adc):
    return (adc / 1023.0) * VREF

# ===============================
# INTERFAZ PARA MAIN
# ===============================
def leer_ecg():
    """
    Devuelve:
    adc_raw, voltaje, voltaje_filtrado
    """
    adc_raw = leer_adc(CANAL_ADC)
    voltaje = adc_a_voltaje(adc_raw)

    buffer_filtro.append(voltaje)
    voltaje_filtrado = sum(buffer_filtro) / len(buffer_filtro)

    return adc_raw, voltaje, voltaje_filtrado

# ===============================
# EJECUCION DIRECTA (standalone)
# ===============================
def iniciar_ecg():
    print("Iniciando lectura de ECG (CTRL+C para salir)")

    with open(ARCHIVO_CSV, mode="w", newline="") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(["timestamp", "adc", "voltaje", "voltaje_filtrado"])

        try:
            while True:
                adc, v, vf = leer_ecg()

                writer.writerow([
                    time.time(),
                    adc,
                    round(v, 4),
                    round(vf, 4)
                ])

                print(
                    f"\rADC: {adc:4d} | V: {v:.3f} V | Vf: {vf:.3f} V   ",
                    end="",
                    flush=True
                )

                time.sleep(DELAY)

        except KeyboardInterrupt:
            apagar_spi()
            print("\n\nMedicion detenida. SPI liberado.")

if __name__ == "__main__":
    iniciar_ecg()
