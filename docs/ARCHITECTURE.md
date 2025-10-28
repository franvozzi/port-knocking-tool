# Arquitectura del Sistema

## Visión General

VPN Port Knocking Tool es una aplicación modular diseñada para facilitar conexiones VPN seguras mediante la técnica de port knocking.

## Arquitectura en Capas
```text
┌─────────────────────────────────────┐
│ UI Layer (Tkinter) │
│ - GUI Principal │
│ - Widgets reutilizables │
└──────────────┬──────────────────────┘
│
┌──────────────▼──────────────────────┐
│ Business Logic Layer │
│ - Port Knocker │
│ - VPN Manager │
│ - Config Manager │
└──────────────┬──────────────────────┘
│
┌──────────────▼──────────────────────┐
│ Infrastructure Layer │
│ - Network diagnostics │
│ - Logging & Metrics │
│ - Security (Crypto) │
└─────────────────────────────────────┘
```


## Módulos Principales

### Core (`src/core/`)
Lógica de negocio principal:
- **PortKnocker**: Implementación del port knocking
- **VPNManager**: Gestión multiplataforma de VPN
- **ConfigManager**: Carga y validación de configuración

### UI (`src/ui/`)
Interfaz de usuario:
- **gui_main.py**: Ventana principal
- **widgets/**: Componentes reutilizables
- **themes.py**: Gestión de temas visuales

### Security (`src/security/`)
Componentes de seguridad:
- **crypto.py**: Cifrado de credenciales

### Network (`src/network/`)
Utilidades de red:
- **diagnostics.py**: Diagnóstico de conectividad
- **circuit_breaker.py**: Patrón de resiliencia

### Monitoring (`src/monitoring/`)
Observabilidad:
- **logger.py**: Logging estructurado
- **metrics.py**: Recolección de métricas

### Utils (`src/utils/`)
Utilidades generales:
- **exceptions.py**: Excepciones personalizadas
- **validators.py**: Validadores
- **constants.py**: Constantes globales

## Flujo de Ejecución

1. Usuario hace click en "Conectar"
2. GUI llama a PortKnocker.execute_sequence()
3. PortKnocker envía knocks al servidor
4. PortKnocker verifica puerto VPN abierto
5. GUI llama a VPNManager.connect()
6. VPNManager establece conexión OpenVPN
7. Métricas y logs son actualizados

## Patrones de Diseño Utilizados

- **Factory Pattern**: `get_vpn_manager()` retorna gestor según OS
- **Circuit Breaker**: Protección contra fallos repetidos
- **Singleton**: Logger y Metrics Collector
- **Strategy Pattern**: VPNManager para cada plataforma

## Dependencias Externas

- **cryptography**: Cifrado de credenciales
- **tkinter**: Interfaz gráfica (incluido en Python)
- **pyinstaller**: Compilación de ejecutables

## Consideraciones de Seguridad

- Credenciales cifradas con Fernet (AES-128)
- Config.json embebido en ejecutable
- Logs con información sensible enmascarada
- Validación estricta de inputs
