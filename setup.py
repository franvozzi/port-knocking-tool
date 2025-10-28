"""
Setup para instalación del paquete
"""
from setuptools import setup, find_packages
from pathlib import Path

# Leer README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="vpn-port-knocking-tool",
    version="2.0.0",
    author="Francisco Vozzi",
    author_email="tu_email@ejemplo.com",
    description="Herramienta de conexión VPN con port knocking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/franvozzi/port-knocking-tool",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Networking",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "cryptography>=41.0.0",
    ],
    entry_points={
        'console_scripts': [
            'vpn-connect=src.main:main',
            'vpn-config=src.cli.configurador_config:main',
            'vpn-import=src.cli.importar_ovpn:main',
        ],
    },
)
