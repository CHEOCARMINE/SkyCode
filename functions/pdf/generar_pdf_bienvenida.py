from fpdf import FPDF
import os

class PDFBienvenida(FPDF):
    def header(self):
        self.set_fill_color(44, 62, 80)  # Azul base
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Bienvenido a SkyCode", ln=True, align='C', fill=True)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Página {self.page_no()} / {{nb}}", align='C')

def generar_pdf_bienvenida(nombre, apellido, matricula, carrera):
    carpeta = "static/pdfs_bienvenida"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    ruta_pdf = os.path.join(carpeta, f"bienvenida_{matricula}.pdf")

    pdf = PDFBienvenida()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_font("Arial", size=12)

    mensaje = f"""
Hola {nombre} {apellido},

¡Nos complace darte la bienvenida a **SkyCode**!

Tu matrícula asignada es: {matricula}
Tu carrera: {carrera}

Desde hoy, formas parte de una comunidad académica enfocada en el crecimiento, el aprendizaje y la excelencia.

En nuestra plataforma podrás consultar tu avance académico, tus materias, calificaciones y mucho más.

No olvides cambiar tu contraseña después de tu primer inicio de sesión por seguridad.

¡Te deseamos mucho éxito en esta nueva etapa académica!

Atentamente,  
Equipo SkyCode
    """

    pdf.multi_cell(0, 10, mensaje.strip())

    pdf.output(ruta_pdf)
    return ruta_pdf
