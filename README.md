# Manual de Ejecución - VPN Port Knocking Tool

**Versión:** 1.0
**Fecha:** Octubre 2025
**Audiencia:** Soporte IT / Administradores de Sistemas

---

## Índice

1. [Requisitos previos](#requisitos-previos)
2. [Configuración inicial](#configuración-inicial)
3. [Generación del ejecutable](#generación-del-ejecutable)
4. [Pruebas](#pruebas)
5. [Distribución a usuarios](#distribución-a-usuarios)
6. [Solución de problemas](#solución-de-problemas)

---

## Requisitos previos

### Software necesario

* Python 3.9+ instalado
* PyInstaller instalado: `pip install pyinstaller`
* Archivo `.ovpn` del servidor VPN
* (Opcional) Archivo de ícono en `resources/icon.ico`

### Estructura del proyecto

```text
port-knocking-tool/
├── dummies/                  # Scripts de prueba
├── src/                      # Código de producción
│   ├── gui_main.py
│   ├── main.py
│   ├── configurador_config.py
│   └── importar_ovpn.py
├── resources/
│   └── icon.ico
└── README.md
```

---

## Configuración inicial

### Paso 1: Importar perfil VPN

Ejecutá el script de importación de perfiles:

```bash
cd src/
python importar_ovpn.py
```

**Acciones del script:**

* Busca archivos `.ovpn` en la carpeta actual
* Si no encuentra ninguno, solicita la ruta del archivo
* Copia el archivo a `src/` y lo renombra a `profile.ovpn`
* (Opcional) Solicita credenciales y crea `credentials.txt`

**Ejemplo de ejecución:**

```text
============================================================
  Configurador de Perfil OpenVPN - VPN Corporativa
============================================================

Paso 1: Importar archivo .ovpn
------------------------------------------------------------

✗ No se encontró ningún archivo .ovpn en la carpeta actual.

Ingrese la ruta del archivo .ovpn que desea importar:
Ruta del archivo .ovpn: ~/VPN/empresa.ovpn

✓ Archivo copiado exitosamente
✓ Archivo renombrado a 'profile.ovpn'

Paso 2: Configurar credenciales
------------------------------------------------------------
Crear credentials.txt? (s/n): s
Usuario VPN: admin
Clave VPN: ********

✓ Archivo credentials.txt creado exitosamente.

============================================================
  Resumen de archivos configurados:
============================================================
  ✓ profile.ovpn (2048 bytes)
  ✓ credentials.txt (18 bytes)

✓ Configuración completada exitosamente.
```

**Archivos generados:**

* `src/profile.ovpn`
* `src/credentials.txt` (opcional)

---

### Paso 2: Configurar port knocking

Ejecutá el script de configuración:

```bash
python configurador_config.py
```

**Acciones del script:**

* Solicita IP pública del servidor
* Solicita secuencia de puertos para knocking
* Solicita intervalo entre knocks
* Solicita puerto final a habilitar (VPN)
* Genera `config.json`

**Ejemplo de ejecución:**

```text
=== Configurador de config.json para Port Knocking ===
IP pública del servidor: 203.0.113.10

Ingrese secuencia de knocks (Enter vacío para terminar):
  Puerto: 7000
  Protocolo (tcp/udp): tcp
  Puerto: 8000
  Protocolo (tcp/udp): tcp
  Puerto:

Intervalo entre knocks en segundos (ej: 0.5): 0.5
Puerto final a habilitar (ej: 1194): 1194

✓ Archivo config.json guardado correctamente.
```

**Archivo generado:**

* `src/config.json`

**Contenido de ejemplo:**

```json
{
  "target_ip": "203.0.113.10",
  "knock_sequence": [
    [7000, "tcp"],
    [8000, "tcp"]
  ],
  "interval": 0.5,
  "target_port": 1194
}
```

---

### Paso 3: Verificar archivos

Antes de compilar, verificá que estén todos los archivos necesarios:

```bash
cd src/
ls -la
```

**Deberías ver:**

* ✅ `gui_main.py`
* ✅ `main.py`
* ✅ `config.json`
* ✅ `profile.ovpn`
* ✅ `credentials.txt` (opcional)

---

## Generación del ejecutable

### Compilación para macOS

```bash
cd ..  # Volver a la raíz del proyecto

pyinstaller --onedir --windowed \
  --name "VPNConnect" \
  --icon="resources/icon.ico" \
  --add-data "src/config.json:." \
  --add-data "src/profile.ovpn:." \
  --add-data "src/credentials.txt:." \
  src/gui_main.py
```

**Resultado:**

* Ejecutable en: `dist/VPNConnect.app`

### Compilación para Windows

```text
pyinstaller --onefile --windowed ^
  --name "VPNConnect" ^
  --icon="resources\icon.ico" ^
  --add-data "src\config.json;." ^
  --add-data "src\profile.ovpn;." ^
  --add-data "src\credentials.txt;." ^
  src\gui_main.py
```

**Resultado:**

* Ejecutable en: `dist\VPNConnect.exe`

### Compilación para Linux

```bash
pyinstaller --onefile --windowed \
  --name "VPNConnect" \
  --add-data "src/config.json:." \
  --add-data "src/profile.ovpn:." \
  --add-data "src/credentials.txt:." \
  src/gui_main.py
```

**Resultado:**

* Ejecutable en: `dist/VPNConnect`

---

## Pruebas

### Probar el ejecutable antes de distribuir

#### macOS

```bash
open dist/VPNConnect.app
```

#### Windows

```text
dist\VPNConnect.exe
```

#### Linux

```bash
chmod +x dist/VPNConnect
./dist/VPNConnect
```

### Checklist de pruebas

* La ventana se abre correctamente
* Botón "Conectar" funciona
* Port knocking se ejecuta (revisar logs)
* OpenVPN se conecta (si hay servidor de prueba)
* Botón "Desconectar" funciona
* Mensajes de error se muestran correctamente

---

## Distribución a usuarios

### macOS

**Opción 1:** Distribuir `.app` directamente

```bash
# Comprimir
zip -r VPNConnect.zip dist/VPNConnect.app
```

Enviar por correo o compartir en red.

**Opción 2:** Crear instalador `.dmg` (avanzado)

```bash
brew install create-dmg
create-dmg 'dist/VPNConnect.app' dist/
```

### Windows

**Opción 1:** Distribuir `.exe` directamente
Enviar `VPNConnect.exe`

**Opción 2:** Crear instalador `.msi` (avanzado)
Usar **Inno Setup** o **WiX Toolset**

### Linux

Distribuir el binario:

```bash
tar -czvf VPNConnect-linux.tar.gz -C dist/ VPNConnect
# O crear .deb/.rpm según distribución
```

---

## Solución de problemas

### Error: "config.json no encontrado"

**Causa:** El archivo no fue embebido correctamente.
**Solución:**

* Verificar que `config.json` existe en `src/`
* Recompilar con el flag `--add-data` correcto

### Error: "profile.ovpn no encontrado"

**Causa:** El archivo `.ovpn` no fue incluido.
**Solución:**

* Ejecutar `python importar_ovpn.py`
* Verificar que `profile.ovpn` existe en `src/`
* Recompilar

### Error: "Port knocking fallido"

**Causa:**

* Secuencia incorrecta
* Servidor no configurado
* Firewall bloqueando

**Solución:**

* Verificar `config.json`
* Probar manualmente con `telnet` o `nc`:

```bash
nc -zv 203.0.113.10 7000
nc -zv 203.0.113.10 8000
```

Verificar configuración del firewall del servidor.

### El ejecutable no se abre en macOS

**Causa:** Permisos de seguridad de macOS.
**Solución:**

```bash
chmod +x dist/VPNConnect.app/Contents/MacOS/VPNConnect
xattr -cr dist/VPNConnect.app
```

Luego intentar abrir con **Ctrl + Click → "Abrir"**.

---

## Actualización de configuración

Para actualizar la configuración (IP, puertos, perfil VPN):

1. Modificar archivos en `src/`:

   * `config.json`
   * `profile.ovpn`
   * `credentials.txt`
2. Recompilar el ejecutable
3. Redistribuir a usuarios

---