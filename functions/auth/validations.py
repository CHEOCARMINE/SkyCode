import re
from datetime import datetime
from models import Alumno, Coordinadores_Directivos  # Se usa para generar la matrícula basada en el último registro

# ----- Generación Automática de Matrícula -----
def generar_matricula():
    """
    Genera la matrícula automáticamente con el formato:
    ALU + año actual + número secuencial (4 dígitos)
    """
    año = datetime.now().year
    ultimo_alumno = Alumno.query.order_by(Alumno.id.desc()).first()
    secuencia = ultimo_alumno.id + 1 if ultimo_alumno else 1
    return f"ALU{año}{secuencia:04d}"

# ----- Validación de CURP -----
CURP_REGEX = r'^[A-Z]{4}\d{6}[HM][A-Z]{2}[A-Z]{3}[0-9A-Z]\d$'
def validate_curp(curp):
    """
    Valida que el CURP cumpla con el formato requerido:
    - 4 letras (iniciales del primer apellido, segundo apellido y nombre)
    - 6 dígitos (fecha de nacimiento en formato YYMMDD)
    - 1 letra para el sexo (H o M)
    - 2 letras para la clave del estado
    - 3 letras (primeras consonantes internas)
    - 1 carácter alfanumérico (homoclave)
    - 1 dígito verificador
    """
    return bool(re.match(CURP_REGEX, curp))

# ----- Validación de Teléfono -----
def validate_telefono(telefono):
    """
    Valida que el teléfono contenga exactamente 10 dígitos.
    """
    return telefono.isdigit() and len(telefono) == 10

# ----- Validación de Correo Electrónico -----
ALLOWED_DOMAINS = {"gmail.com", "hotmail.com", "live.com.mx", "red.unid.mx"}
def validate_correo(correo):
    """
    Valida que el correo contenga '@' y que el dominio esté permitido.
    """
    if "@" not in correo:
        return False
    usuario, dominio = correo.split("@", 1)
    return dominio.lower() in ALLOWED_DOMAINS

# ----- Validación de Archivos PDF y Tamaño -----
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB
def allowed_file(filename):
    """
    Verifica que la extensión del archivo sea PDF.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file(file_obj):
    """
    Valida que el archivo:
      - Sea de extensión PDF.
      - No exceda el tamaño máximo permitido.
    """
    if not allowed_file(file_obj.filename):
        return False, "El archivo debe ser PDF."
    
    file_obj.seek(0, 2)  # Mover el cursor al final del archivo
    file_size = file_obj.tell()
    file_obj.seek(0)     # Regresar el cursor al inicio
    
    if file_size > MAX_FILE_SIZE:
        return False, "El archivo excede el tamaño permitido (2MB o 2,000KB)."
    
    return True, ""

# ----- Validación de Solo Letras -----
def validate_letters(text, required=True):
    """
    Valida que el texto contenga únicamente letras y espacios.
    
    :param text: Cadena a validar.
    :param required: Si es True, se exige al menos un carácter; si es False, se permite vacío.
    :return: True si cumple, False en caso contrario.
    """
    pattern = r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$' if required else r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]*$'
    return bool(re.match(pattern, text))

# ----- Validación de Código Postal -----
def validate_postal_code(cp):
    """
    Valida que el código postal contenga exactamente 5 dígitos.
    """
    pattern = r'^\d{5}$'
    return bool(re.match(pattern, cp))

# ----- Validación para campos alfanuméricos (por ejemplo, número de calle) -----
def validate_alphanumeric(text, required=True):
    """
    Valida que el texto contenga únicamente caracteres alfanuméricos, espacios y guiones.
    
    :param text: La cadena a validar.
    :param required: Si es True, se exige al menos un carácter; si es False, se permite vacío.
    :return: True si cumple, False en caso contrario.
    """
    pattern = r'^[A-Za-z0-9\s\-]+$' if required else r'^[A-Za-z0-9\s\-]*$'
    return bool(re.match(pattern, text))

# ----- Generación Automática de Matrícula para Coordinadores y Directivos -----
def generar_matricula_coordinador_directivo(tipo_usuario: str) -> str:
    """
    Genera la matrícula automáticamente para Coordinadores y Directivos con el formato:
    <Prefijo><Año><Número secuencial de 4 dígitos>
    
    Ejemplos:
      COO20250001
      DIR20250001

    :param tipo_usuario: 'COO' para coordinadores o 'DIR' para directivos.
    :return: Matrícula generada.
    """
    if tipo_usuario not in ['COO', 'DIR']:
        raise ValueError("El tipo de usuario debe ser 'COO' o 'DIR'.")
    
    year = datetime.now().year
    prefix = f"{tipo_usuario}{year}"
    
    # Consulta el último registro cuya matrícula comience con el prefijo
    ultimo_registro = Coordinadores_Directivos.query.filter(
        Coordinadores_Directivos.matricula.like(f"{prefix}%")
    ).order_by(Coordinadores_Directivos.matricula.desc()).first()
    
    if ultimo_registro:
        ultimo_secuencia = int(ultimo_registro.matricula[-4:])
    else:
        ultimo_secuencia = 0
    
    nuevo_secuencia = ultimo_secuencia + 1
    matricula = f"{prefix}{nuevo_secuencia:04d}"
    
    return matricula