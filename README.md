# 🧱 PortKnocker - Herramienta de Port Knocking para MikroTik

## 📖 Descripción
**PortKnocker** es una herramienta avanzada en **Python** diseñada para ejecutar secuencias de *Port Knocking* en routers **MikroTik** o cualquier otro firewall compatible. 

Permite enviar secuencias TCP (solo SYN) o UDP, registrar logs detallados y verificar si un puerto objetivo se abre correctamente tras el knocking. Es ideal para entornos de red donde se utilizan mecanismos de seguridad basados en listas dinámicas de IP (address lists).

---

## ⚙️ Características principales
- Envío de knocks TCP (solo SYN) y UDP.
- Modo interactivo con validación de entradas.
- Verificación progresiva del puerto objetivo (2s, 5s, 10s).
- Registro detallado de logs con timestamp.
- Guardado/carga de configuraciones JSON.
- Soporte multiplataforma (Windows / Linux / macOS).

---

## 🧩 Requisitos

- **Python 3.8+**
- Permisos de red/sockets (puede requerir ejecución como administrador en algunos entornos)

Instalación recomendada de dependencias:

```bash
pip install -r requirements.txt  # (si corresponde)
```

---

## 🚀 Uso

Ejecuta el script principal:

```bash
python portknocker.py
```

Sigue las instrucciones interactivas:
1. Ingresa la IP del dispositivo MikroTik.
2. Define la cantidad de knocks y sus puertos/protocolos.
3. Configura el intervalo entre knocks.
4. (Opcional) Especifica un puerto objetivo para verificar su apertura.
5. Guarda la configuración si deseas reutilizarla.

---

## 🧠 Ejemplo de ejecución

```bash
======================================================
HERRAMIENTA DE PORT KNOCKING - MIKROTIK
Modo: TCP SYN-only (primer handshake)
======================================================

Ingrese la IP del MikroTik: 203.0.113.10
Cantidad de knocks: 3

Knock #1:
  Puerto: 1234
  Protocolo: TCP

Knock #2:
  Puerto: 5678
  Protocolo: UDP

Knock #3:
  Puerto: 9100
  Protocolo: TCP

Tiempo entre knocks (segundos): 1.5
Verificar apertura de puerto despues del knocking? (s/n): s
Puerto que deberia abrirse: 22
Tipo de verificacion: 1

Ejecutar secuencia? (s/n): s
```

Resultado:
```
Knock TCP SYN puerto 1234 - Tiempo: 0.45ms
Knock UDP puerto 5678 - Tiempo: 0.12ms
Knock TCP SYN puerto 9100 - Tiempo: 0.47ms

[*] Verificando apertura del puerto 22 con delays progresivos...
[1/3] Esperando 2s antes de verificar...
[+] ABIERTO despues de 2s de delay acumulado ✅
```

---

## 💾 Archivos generados

- `portknock_config.json` → configuración guardada.
- `portknock_<ip>_<timestamp>.log` → registro detallado de ejecución.

Ejemplo de log:
```text
[12:31:45.103] [INFO] Knock TCP SYN puerto 1234 - Tiempo: 0.43ms
[12:31:46.621] [INFO] Knock UDP puerto 5678 - Tiempo: 0.15ms
[12:31:48.001] [INFO] Puerto 22 abierto despues de 5.00s
```

---

## 🧱 Ejemplo de configuración JSON

```json
{
  "target_ip": "203.0.113.10",
  "knock_sequence": [[1234, "tcp"], [5678, "udp"], [9100, "tcp"]],
  "interval": 1.5,
  "target_port": 22
}
```

Carga automática al iniciar si el archivo `portknock_config.json` existe.

---

## ⚠️ Advertencias

- El uso indebido de port knocking en redes externas puede ser considerado actividad intrusiva. Úselo únicamente con dispositivos bajo su control o autorización.
- MikroTik requiere configuración previa de reglas firewall y listas de direcciones (*address lists*).

---

## 🧩 Estructura del proyecto

```
portknocker/
├── portknocker.py           # Script principal
├── portknock_config.json    # Configuración persistente (opcional)
├── requirements.txt         # Dependencias (opcional)
├── logs/                    # Carpeta sugerida para registros
└── README.md                # Este archivo
```

---

## 🧑‍💻 Autor
**Francisco Vozzi**  
🔗 GitHub: [franvozzi](https://github.com/franvozzi)

---

## 🛠️ Licencia

Este proyecto se distribuye bajo la licencia **MIT**. Puedes usarlo, modificarlo y distribuirlo libremente, siempre que se mantenga la atribución correspondiente.
