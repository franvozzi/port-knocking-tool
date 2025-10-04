# Port Knocking Tool para MikroTik

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)

Herramienta en Python para ejecutar secuencias de port knocking hacia equipos MikroTik, permitiendo configurar cada knock individualmente con protocolo TCP o UDP.

## Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Testing](#testing)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Ejemplos](#ejemplos)
- [Licencia](#licencia)

## Descripción

Esta herramienta implementa un cliente de port knocking que permite ejecutar secuencias de "toques" a puertos específicos en un router MikroTik configurado con reglas de firewall de port knocking. Cada knock puede ser configurado individualmente con protocolo TCP o UDP, proporcionando mayor flexibilidad y seguridad.

El port knocking es una técnica de seguridad que oculta servicios de red hasta que se recibe una secuencia específica de intentos de conexión a puertos predefinidos.

## Características

- ✅ Soporte para knocks TCP y UDP en la misma secuencia
- ✅ Configuración individual de protocolo por cada knock
- ✅ Intervalo de tiempo configurable entre knocks
- ✅ Interfaz de línea de comandos intuitiva
- ✅ Validación de entrada de usuario
- ✅ Salida con formato visual claro
- ✅ Suite completa de tests (unitarios + integración)
- ✅ Sin dependencias externas (solo librería estándar de Python)

## Requisitos

- Python 3.8 o superior
- Sistema operativo: Linux, macOS, o Windows
- Router MikroTik configurado con reglas de port knocking

## Instalación

### Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/port-knocking-mikrotik.git
cd port-knocking-mikrotik

```
### Verificar instalación de Python
```
python3 --version
```
## Uso

### Ejecución básica
```bash
python3 main.py
```
### Flujo de uso interactivo

1. **Ingresar IP del MikroTik**
Ingrese la IP del MikroTik: xxx.xxx.xx.x
2. **Especificar cantidad de knocks**

    Cantidad de knocks: 3

    Knock #1:
    Puerto: 8881
    Protocolo (TCP/UDP): tcp

    Knock #2:
    Puerto: 5555
    Protocolo (TCP/UDP): udp

    Knock #3:
    Puerto: 2222
    Protocolo (TCP/UDP): tcp

4. **Definir intervalo entre knocks**
Tiempo entre knocks (segundos): 0.5

5. **Confirmar y ejecutar**
¿Ejecutar secuencia? (s/n): s

### Ejemplo de salida
============================================================
INICIANDO PORT KNOCKING A 192.168.88.1
Total de knocks: 3 | Intervalo: 0.5s
[1/3] Knock TCP en puerto 8881... ✓
[2/3] Knock UDP en puerto 5555... ✓
[3/3] Knock TCP en puerto 2222... ✓

============================================================
SECUENCIA COMPLETADA - Ahora podés conectarte al servicio