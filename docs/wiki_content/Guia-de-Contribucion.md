
# Guía de Contribución

¡Gracias por tu interés en contribuir a este proyecto! A continuación, encontrarás una guía para ayudarte a empezar.

## Cómo Contribuir

Aceptamos contribuciones en forma de `pull requests`. Si quieres añadir una nueva función, corregir un error o mejorar la documentación, sigue estos pasos:

1.  **Crea un `fork` del repositorio:** Haz clic en el botón "Fork" en la esquina superior derecha de la página del repositorio.
2.  **Clona tu `fork`:**
    ```bash
    git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
    ```
3.  **Crea una nueva rama:**
    ```bash
    git checkout -b nombre-de-tu-rama
    ```
4.  **Realiza tus cambios:** Implementa tu nueva función o corrección de error.
5.  **Añade y confirma tus cambios:**
    ```bash
    git add .
    git commit -m "feat: Añade una nueva función increíble"
    ```
6.  **Envía tus cambios a tu `fork`:**
    ```bash
    git push origin nombre-de-tu-rama
    ```
7.  **Crea un `pull request`:** Ve a la página del repositorio original y crea un `pull request` desde tu `fork`.

## Configuración del Entorno de Desarrollo

Para trabajar en el proyecto, necesitarás tener Python 3.9+ instalado. Sigue estos pasos para configurar tu entorno:

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
    cd TU_REPOSITORIO
    ```

2.  **Crea un entorno virtual:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # En Windows: .venv\Scripts\activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    ```

4.  **Ejecuta las pruebas:**
    Para asegurarte de que todo está configurado correctamente, ejecuta el conjunto de pruebas:
    ```bash
    python -m pytest
    ```

## Convenciones de Código

- **Estilo de Código:** Seguimos el estilo de código `PEP 8`. Te recomendamos usar un linter como `flake8` o `pylint` para asegurarte de que tu código sigue las convenciones.
- **Mensajes de Commit:** Usamos el formato de "Conventional Commits". Por ejemplo:
    - `feat:` para nuevas funciones.
    - `fix:` para correcciones de errores.
    - `docs:` para cambios en la documentación.
    - `test:` para añadir o mejorar pruebas.
- **Documentación:** Si añades una nueva función, por favor, asegúrate de documentarla.

¡Gracias de nuevo por tu contribución!
