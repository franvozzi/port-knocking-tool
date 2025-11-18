# ¡Bienvenido a la Wiki del Proyecto VPN Port Knocking!

Este proyecto proporciona una solución de seguridad multicapa para el acceso a VPNs corporativas, combinando la autenticación de dos factores (2FA) con TOTP, el "IP whitelisting" dinámico y el "port knocking".

## Navegación

- **[Arquitectura del Proyecto](Arquitectura-del-Proyecto.md)**: Entiende cómo funcionan juntos el cliente, el servidor y el router.
- **[Guía de Contribución](Guia-de-Contribucion.md)**: ¿Quieres colaborar? Aquí encontrarás todo lo que necesitas saber.
- **[Manual de Administrador](Manual-Administrador.md)**: Instrucciones detalladas para configurar el sistema completo.
- **[Manual de Usuario Final](Manual-Usuario-Final.md)**: Una guía sencilla para los usuarios que se conectan a la VPN.

## ¿Qué Problema Resuelve Este Proyecto?

En un entorno corporativo, la seguridad del acceso remoto es fundamental. Una VPN es un buen primer paso, pero puede ser vulnerable a ataques de fuerza bruta o al robo de credenciales. Este proyecto añade dos capas adicionales de seguridad:

1.  **Port Knocking**: El puerto de la VPN permanece cerrado para el mundo exterior hasta que se realiza una secuencia secreta de "golpes" a otros puertos.
2.  **2FA con TOTP**: Antes de que el "port knocking" sea siquiera posible, el usuario debe verificar su identidad con un código de un solo uso, y su IP es autorizada temporalmente en el firewall.

Esto crea una defensa en profundidad que hace que el acceso no autorizado sea extremadamente difícil.

## Índice automático

Accede rápidamente a las páginas principales de la Wiki:

- [Arquitectura (detallada)](architecture.md)
- [Arquitectura del Proyecto](Arquitectura-del-Proyecto.md)
- [Guía de Contribución](Guia-de-Contribucion.md)
- [Manual de Administrador: Configuración de 2FA con TOTP y Port Knocking](Manual-Administrador.md)
- [Manual de Usuario: Conexión Segura a la VPN Corporativa](Manual-Usuario-Final.md)
- [Testing](testing.md)

Si añades nuevas páginas a `docs/wiki/` puedes regenerar este índice automáticamente ejecutando `scripts/generate_wiki_toc.py`.
## Navegación

- **[Arquitectura del Proyecto](arquitectura-del-proyecto.md)**: Entiende cómo funcionan juntos el cliente, el servidor y el router.
- **[Guía de Contribución](guia-de-contribucion.md)**: ¿Quieres colaborar? Aquí encontrarás todo lo que necesitas saber.
- **[Manual de Administrador](manual-administrador.md)**: Instrucciones detalladas para configurar el sistema completo.
- **[Manual de Usuario Final](manual-usuario-final.md)**: Una guía sencilla para los usuarios que se conectan a la VPN.
- **[Arquitectura (detallada)](architecture.md)**: Diagrama y despiece por módulos.
- **[Testing](testing.md)**: Cómo ejecutar las pruebas del proyecto.

## ¿Qué Problema Resuelve Este Proyecto?

En un entorno corporativo, la seguridad del acceso remoto es fundamental. Una VPN es un buen primer paso, pero puede ser vulnerable a ataques de fuerza bruta o al robo de credenciales. Este proyecto añade dos capas adicionales de seguridad:

1.  **Port Knocking**: El puerto de la VPN permanece cerrado para el mundo exterior hasta que se realiza una secuencia secreta de "golpes" a otros puertos.
2.  **2FA con TOTP**: Antes de que el "port knocking" sea siquiera posible, el usuario debe verificar su identidad con un código de un solo uso, y su IP es autorizada temporalmente en el firewall.

Esto crea una defensa en profundidad que hace que el acceso no autorizado sea extremadamente difícil.
# ¡Bienvenido a la Wiki del Proyecto VPN Port Knocking!

Este proyecto proporciona una solución de seguridad multicapa para el acceso a VPNs corporativas, combinando la autenticación de dos factores (2FA) con TOTP, el "IP whitelisting" dinámico y el "port knocking".

## Navegación

- **[Arquitectura del Proyecto](Arquitectura-del-Proyecto.md)**: Entiende cómo funcionan juntos el cliente, el servidor y el router.
- **[Guía de Contribución](Guia-de-Contribucion.md)**: ¿Quieres colaborar? Aquí encontrarás todo lo que necesitas saber.
- **[Manual de Administrador](Manual_Administrador_2FA.md)**: Instrucciones detalladas para configurar el sistema completo.
- **[Manual de Usuario Final](Manual_Usuario_Final.md)**: Una guía sencilla para los usuarios que se conectan a la VPN.

## ¿Qué Problema Resuelve Este Proyecto?

En un entorno corporativo, la seguridad del acceso remoto es fundamental. Una VPN es un buen primer paso, pero puede ser vulnerable a ataques de fuerza bruta o al robo de credenciales. Este proyecto añade dos capas adicionales de seguridad:

1.  **Port Knocking**: El puerto de la VPN permanece cerrado para el mundo exterior hasta que se realiza una secuencia secreta de "golpes" a otros puertos.
2.  **2FA con TOTP**: Antes de que el "port knocking" sea siquiera posible, el usuario debe verificar su identidad con un código de un solo uso, y su IP es autorizada temporalmente en el firewall.

Esto crea una defensa en profundidad que hace que el acceso no autorizado sea extremadamente difícil.
