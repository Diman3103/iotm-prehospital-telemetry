# 🏥 Plataforma IoMT de Telemetría Prehospitalaria

## Monitor de Atención Telemétrica 107

Prototipo de una plataforma de **Internet de las Cosas Médicas (IoMT)** orientada a la adquisición, procesamiento y visualización de signos vitales durante el traslado prehospitalario.

El sistema fue desarrollado como **Proyecto Final de la carrera de Ingeniería en Computación de la Universidad Nacional de Rafaela (UNRaf)** y está orientado al contexto operativo del **Servicio Integrado de Emergencias Sanitarias (SIES 107) de Rafaela, Santa Fe**.

---

## 🎯 Problema

Durante el traslado prehospitalario, la información sobre el estado del paciente puede depender del registro manual y de la comunicación verbal al momento del arribo hospitalario.

Esto dificulta la disponibilidad anticipada de información biomédica y puede generar pérdida de trazabilidad, especialmente en escenarios donde la conectividad es limitada.

La propuesta busca abordar este problema mediante un nodo de procesamiento local capaz de adquirir, procesar, almacenar y exponer información biomédica durante el traslado.

---

## 💡 Solución propuesta

La plataforma utiliza una **Raspberry Pi 5 como Gateway IoMT y nodo de Edge Computing**.

El sistema integra sensores biomédicos para adquirir:

- ❤️ Señal electrocardiográfica (ECG)
- 🫁 Saturación de oxígeno (SpO₂)
- 🌡️ Temperatura corporal
- 💓 Frecuencia cardíaca

Los datos son procesados localmente y almacenados en una base de datos SQLite antes de ser expuestos mediante una API REST.

La arquitectura incorpora un mecanismo **Store and Forward**, permitiendo conservar las mediciones localmente ante interrupciones de conectividad.

---

## 🏗️ Arquitectura

La plataforma se organiza conceptualmente en tres capas:

```text
┌──────────────────────────────────────────────┐
│              ADQUISICIÓN                     │
│                                              │
│  AD8232 ─────┐                               │
│  MAX30100 ───┼──> Raspberry Pi 5             │
│  NTC ────────┘       Gateway IoMT            │
│                         │                    │
└─────────────────────────┼────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────┐
│        PROCESAMIENTO Y PERSISTENCIA          │
│                                              │
│  Validación → Normalización → SQLite         │
│                         │                    │
│                  Store & Forward             │
└─────────────────────────┼────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────┐
│           ENTREGA Y VISUALIZACIÓN            │
│                                              │
│              FastAPI / REST API              │
│                     │                        │
│                     ▼                        │
│               Dashboard Web                  │
└──────────────────────────────────────────────┘
```
---
## 🔧 Hardware
### Unidad de procesamiento
* Raspberry Pi 5
* Raspberry Pi OS
* GPIO
### Adquisición de señales
* AD8232 — Electrocardiografía
* MAX30100 — Oximetría y frecuencia cardíaca
* NTC — Medición de temperatura
* MCP3008 — Conversión analógico-digital
### Comunicación
* SPI — Comunicación con el MCP3008
* I²C — Comunicación con el MAX30100

El MCP3008 permite digitalizar las señales analógicas provenientes de los sensores conectados a la Raspberry Pi.

---

## 💻 Software

El sistema fue desarrollado principalmente utilizando:

* Python
* FastAPI
* SQLite
* REST API
* HTML / JavaScript
* Linux / Raspberry Pi OS

La arquitectura de software fue diseñada de manera modular, separando la adquisición de cada sensor del procesamiento, almacenamiento y exposición de los datos.

---

## 🔄 Flujo de datos

El funcionamiento general del sistema es:

```text
Sensores
   │
   ▼
Adquisición
   │
   ▼
Procesamiento local
   │
   ├── Validación
   ├── Normalización
   └── Detección de lecturas inválidas
   │
   ▼
SQLite
   │
   ├── Conectividad disponible ──> API / transmisión
   │
   └── Sin conectividad ─────────> Almacenamiento local
                                      │
                                      ▼
                              Store & Forward
   │
   ▼
Dashboard Web

```
El proceso principal coordina la adquisición de los diferentes sensores mediante procesos independientes, permitiendo mantener la lectura de las variables sin bloquear el resto del sistema.

## 🛡️ Resiliencia y seguridad

Uno de los aspectos centrales del proyecto es la capacidad de continuar funcionando ante problemas de conectividad.

Las mediciones se almacenan localmente en SQLite antes de cualquier intento de transmisión, permitiendo conservar los datos durante interrupciones de comunicación.

La plataforma también incorpora un mecanismo básico de autenticación para restringir el acceso a la información expuesta por la API.

Para una implementación productiva serían necesarias medidas adicionales de seguridad, cifrado, gestión de identidades y cumplimiento de los requisitos regulatorios correspondientes.

---

## 🔗 Interoperabilidad

La estructura de los datos fue diseñada considerando los lineamientos del estándar HL7/FHIR, con el objetivo de facilitar una futura integración con sistemas de Historia Clínica Electrónica.

La implementación completa de una infraestructura hospitalaria interoperable no forma parte del alcance del prototipo.

## 🧪 Validación

El prototipo fue sometido a pruebas funcionales y escenarios controlados orientados a evaluar:

* estabilidad del hardware;
* continuidad de adquisición;
* procesamiento de señales;
* persistencia de datos;
* comportamiento ante pérdida de conectividad;
* recuperación de información;
* funcionamiento de la interfaz de visualización.

El proyecto se enfoca en la validación técnica y funcional del sistema, y no en la validación clínica estadística de los datos obtenidos.

---

## 📚 Contexto académico

Este proyecto corresponde al Proyecto Final de la carrera de Ingeniería en Computación de la Universidad Nacional de Rafaela (UNRaf).

Autor: Diman Paredes

Título: Ingeniería en Computación

Proyecto: Plataforma IoMT de Telemetría Prehospitalaria

Ubicación: Rafaela, Santa Fe, Argentina

---

## 🚧 Alcance y limitaciones

El proyecto corresponde a un prototipo académico y experimental.

Quedan fuera del alcance:

* validación clínica estadística;
* diagnóstico médico mediante inteligencia artificial;
* despliegue a escala provincial;
* integración completa con sistemas hospitalarios productivos;
* certificación como dispositivo médico comercial;
* implementación productiva de una infraestructura Cloud hospitalaria.

---

## 🔮 Trabajos futuros

Entre las posibles líneas de evolución del proyecto se encuentran:

* incorporación de MQTT para comunicaciones IoMT;
* integración con sistemas hospitalarios;
* ampliación de los mecanismos de seguridad;
* mejoras en la gestión de identidades y cifrado;
* despliegue de infraestructura Cloud;
* incorporación de nuevos sensores;
* ampliación de las capacidades de telemetría;
* desarrollo de mecanismos avanzados de interoperabilidad;
* evaluación en escenarios operativos de mayor escala.

---

## 📖 Documentación

La documentación completa del proyecto se encuentra en el informe final de tesis.

El repositorio contiene el código correspondiente a la plataforma de adquisición y procesamiento desarrollada durante el proyecto.

---

## 👨‍💻 Autor

### Diman Paredes

Proyecto Final — Ingeniería en Computación
Universidad Nacional de Rafaela

