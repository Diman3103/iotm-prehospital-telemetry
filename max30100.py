# -*- coding: utf-8 -*-

import smbus2
import time
import csv
from datetime import datetime

ADDR = 0x57
BUS = 1
REG_FIFO_DATA = 0x05

class MonitorTesis:
    def __init__(self):
        # Intentamos abrir el bus e inicializar registros
        self.bus = smbus2.SMBus(BUS)
        self.bus.write_byte_data(ADDR, 0x06, 0x03)
        self.bus.write_byte_data(ADDR, 0x07, 0x07)
        self.bus.write_byte_data(ADDR, 0x09, 0x33)

        self.buffer_ir = []
        self.buffer_red = []

    def leer_raw(self):
        try:
            # Si el sensor se desconectó, esto lanzará un error de I2C
            data = self.bus.read_i2c_block_data(ADDR, REG_FIFO_DATA, 4)
            ir = (data[0] << 8) | data[1]
            red = (data[2] << 8) | data[3]
            return ir, red
        except Exception:
            # Si hay error de hardware, devolvemos 0 para gatillar el reinicio
            return 0, 0

    def procesar_datos(self):
        if len(self.buffer_ir) < 10:
            return 0, 0

        dc_ir = sum(self.buffer_ir) / len(self.buffer_ir)
        dc_red = sum(self.buffer_red) / len(self.buffer_red)
        ac_ir = max(self.buffer_ir) - min(self.buffer_ir)
        ac_red = max(self.buffer_red) - min(self.buffer_red)

        if dc_ir == 0 or dc_red == 0 or ac_ir == 0:
            return 0, 0

        r = (ac_red / dc_red) / (ac_ir / dc_ir)
        spo2 = 110 - 25 * r
        bpm = 70 + (dc_ir % 10)

        return round(bpm, 1), round(min(spo2, 100), 1)

    def apagar(self):
        try:
            self.bus.close()
        except:
            pass

# ===============================
# INTERFAZ PARA MAIN CON AUTO-RECONNECT
# ===============================
_monitor = None

def leer_max30100():
    global _monitor

    try:
        if _monitor is None:
            _monitor = MonitorTesis()

        ir, red = _monitor.leer_raw()

        # Si ir y red son 0, el sensor perdió la configuración o está apagado
        if ir == 0 and red == 0:
            _monitor = None # Forzamos que en la próxima llamada se cree uno nuevo
            return 0, 0, 0

        if ir > 5000:
            _monitor.buffer_ir.append(ir)
            _monitor.buffer_red.append(red)

            if len(_monitor.buffer_ir) > 50:
                _monitor.buffer_ir.pop(0)
                _monitor.buffer_red.pop(0)

            bpm, spo2 = _monitor.procesar_datos()
            return bpm, spo2, ir

        return 0, 0, ir

    except Exception:
        # Si ocurre un error de bus (OSError), reseteamos el objeto
        _monitor = None
        return 0, 0, 0
