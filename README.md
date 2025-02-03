# Sistema de Control de Alumnos

## SkyCode

El **Sistema de Control de Alumnos** es una plataforma integral diseñada para gestionar de manera eficiente y centralizada los datos académicos, administrativos y de avance de los estudiantes en una institución educativa. Este sistema está pensado para facilitar la interacción entre alumnos, coordinadores y directivos, proporcionando acceso a información clave como:

- Inscripción de materias
- Historial académico
- Generación de reportes
- Evaluación docente
- Y otras funcionalidades relevantes

Además, el sistema está diseñado para integrarse con un sistema externo de control de docentes, asegurando la sincronización de datos clave como:

- Horarios
- Calificaciones
- Materias activas

## Cómo Clonar el Proyecto

Para obtener una copia local del proyecto, sigue estos pasos:

1. Clona el repositorio desde GitHub:

    ```bash
    git clone https://github.com/CHEOCARMINE/SkyCode.git
    ```

2. Accede al directorio del proyecto:

    ```bash
    cd SkyCode
    ```

3. Sigue los pasos de configuración mencionados más abajo.

## Configuración del Entorno

A continuación, se detallan los pasos necesarios para configurar el proyecto en tu máquina local:

### 1. Verificar la Versión de Python
Asegúrate de tener instalada la versión **Python 3.13.1** (o una versión compatible). Puedes verificar tu versión de Python ejecutando el siguiente comando:

    ```bash
    python --version
    ```

Si no tienes la versión correcta, descárgala e instálala desde [python.org](https://www.python.org/).

### 2. Crear un Entorno Virtual
Es recomendable usar un entorno virtual para aislar las dependencias del proyecto. Para crearlo y activarlo, sigue estos pasos:

#### En Windows:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

#### En macOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

### 3. Instalar Dependencias
Instala las dependencias del proyecto utilizando el archivo `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

### 4. Configurar Variables de Entorno
El proyecto utiliza un archivo `.env` para manejar configuraciones sensibles. Sigue estos pasos:

- Copia el archivo `.env.example` y renómbralo a `.env`:

    ```bash
    cp .env.example .env
    ```

- Abre el archivo `.env` y configura las variables de entorno con los valores adecuados. Por ejemplo:

    ```
    SECRET_KEY=tu_clave_secreta_aqui
    DATABASE_URI=tu_url_de_base_de_datos_aqui
    DEBUG=True
    ```

**Nota**: Nunca compartas el archivo `.env` ni subas credenciales al repositorio.
