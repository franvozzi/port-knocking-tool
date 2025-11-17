"""
Módulo TOTP eliminado del MVP.

Este archivo existió originalmente para proporcionar generación y verificación
de TOTP/2FA. El MVP actual ha removido la funcionalidad 2FA para simplificar el
flujo: Port Knocking + VPN. Mantener este stub para evitar errores si algún
archivo intenta importarlo accidentalmente.
"""

raise ImportError("El módulo 'totp_manager' ha sido retirado en el MVP sin 2FA.")
