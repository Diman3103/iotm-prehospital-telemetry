# -*- coding: utf-8 -*-

# Diccionario global que mantiene los últimos valores leídos de los sensores
# Se agregó 'sensores_online' para el sistema de autodiagnóstico.
_estado_actual = {
    "sensores_online": True,
    "bpm": 0,
    "spo2": 0,
    "ir": 0,
    "temperatura": 0.0,
    "ecg": {
        "adc": 0,
        "voltaje": 0.0,
        "voltaje_filtrado": 0.0
    }
}

def actualizar(nuevos_datos):
    """
    Actualiza el estado global con los nuevos valores de los sensores.
    Se usa para comunicar el proceso de captura (main.py) con la API.
    """
    global _estado_actual
    _estado_actual.update(nuevos_datos)

def obtener_estado():
    """
    Devuelve el estado actual completo almacenado en la RAM.
    """
    return _estado_actual
