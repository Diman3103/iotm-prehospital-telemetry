# -*- coding: utf-8 -*-

import spidev
import time
import math

# ===============================
# PARAMETROS DEL CIRCUITO
# ===============================
R_FIXED = 10000.0
B_COEFFICIENT = 3950.0

R_CAL = 11000.0
T_CAL = 36.0 + 273.15

# ===============================
# INTERFAZ SPI (lazy)
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
    global _spi
    try:
        if _spi:
            _spi.close()
            _spi = None
    except:
        pass

# ===============================
# FUNCIONES
# ===============================
def read_adc(channel):
    spi = _get_spi()
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    return ((r[1] & 3) << 8) + r[2]

def calcular_temperatura(adc_value):
    if adc_value <= 0 or adc_value >= 1023:
        return None

    resistance = R_FIXED * (adc_value / (1023.0 - adc_value))

    steinhart = math.log(resistance / R_CAL)
    steinhart /= B_COEFFICIENT
    steinhart += 1.0 / T_CAL
    steinhart = 1.0 / steinhart

    return steinhart - 273.15

# ===============================
# INTERFAZ PARA MAIN
# ===============================
def leer_temperatura():
    adc_value = read_adc(0)
    temp = calcular_temperatura(adc_value)
    return temp if temp is not None else 0.0

# ===============================
# EJECUCION DIRECTA
# ===============================
def iniciar_temperatura():
    print("Iniciando medicion de temperatura (CTRL+C para salir)")

    try:
        while True:
            adc = read_adc(0)
            temp = calcular_temperatura(adc)

            if temp is not None:
                print(
                    f"\rADC: {adc:4d} | Temp: {temp:6.2f} C      ",
                    end="",
                    flush=True
                )

            time.sleep(1)

    except KeyboardInterrupt:
        apagar_spi()
        print("\nProceso terminado. SPI liberado.")

if __name__ == "__main__":
    iniciar_temperatura()
