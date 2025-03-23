import matplotlib
matplotlib.use('Agg')  

import os
from fpdf import FPDF
import matplotlib.pyplot as plt
import os
import uuid

# ------------------------------------------------------------
# Route para descargar el reporte estadistico en PDF
# ------------------------------------------------------------

class PDF(FPDF):
    def header(self):
        """Encabezado del PDF"""
        self.set_font("Arial", "B", 16)
        self.set_fill_color(44, 62, 80)  # Azul base #2c3e50
        self.set_text_color(255, 255, 255)  # Texto blanco
        self.cell(200, 10, "Reporte Estadístico - SkyCode", ln=True, align='C', fill=True)
        self.ln(10)

    def footer(self):
        """Pie de página con número de página"""
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Página {self.page_no()} / {{nb}}", align='C')

def generar_pdf_reporte(datos_reporte):
    """
    Genera un PDF con los datos estadísticos del reporte.
    """
    report_dir = "static/reports"
    report_path = os.path.join(report_dir, "reporte_estadistico.pdf")

    # 🔥 Verificar si la carpeta 'static/reports' existe, si no, la crea.
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    # 📄 Crear el PDF con márgenes y alineación mejorada
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)  # Ajusta el margen inferior
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # 🔹 Total de Alumnos y Egresados
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Total de Alumnos: {datos_reporte.get('total_alumnos', 0)}", ln=True, align='C')
    pdf.cell(0, 10, f"Total de Egresados: {datos_reporte.get('total_egresados', 0)}", ln=True, align='C')

    # 🔹 Promedio Global
    promedio_global = datos_reporte.get("promedio_global", 0)
    pdf.set_font("Arial", "B", 12)
    pdf.ln(5)
    pdf.cell(0, 10, f"Promedio Global: {round(promedio_global, 2) if isinstance(promedio_global, (int, float)) else 'N/A'}", ln=True, align='C')

    pdf.ln(10)  # Espacio antes de la tabla

    # 🔹 Datos por carrera
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Promedio por Carrera", ln=True, align='C')

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(44, 62, 80)  # Azul base #2c3e50
    pdf.set_text_color(255, 255, 255)  # Texto blanco

    pdf.cell(90, 10, "Carrera", border=1, align='C', fill=True)
    pdf.cell(50, 10, "Promedio", border=1, align='C', fill=True)
    pdf.cell(50, 10, "Egresados", border=1, align='C', fill=True)
    pdf.ln()

    # 🔹 Agregar datos
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)  # Texto negro
    carreras = datos_reporte.get("promedios_carreras", {})

    if not carreras:
        pdf.cell(190, 10, "No hay datos disponibles.", ln=True, align='C')
    else:
        for carrera, promedio in carreras.items():
            pdf.cell(90, 10, carrera, border=1, align='C')
            pdf.cell(50, 10, f"{round(promedio, 2) if isinstance(promedio, (int, float)) else 'N/A'}", border=1, align='C')
            pdf.cell(50, 10, "N/A", border=1, align='C')  # Si hay egresados, puedes agregarlo aquí
            pdf.ln()

    pdf.output(report_path)

    return report_path  # 📂 Retorna la ruta del PDF generado.

# ------------------------------------------------------------
# Route para descargar el reporte por materia en PDF
# ------------------------------------------------------------

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.set_fill_color(44, 62, 80)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, "Reporte por Materia - SkyCode", ln=True, align="C", fill=True)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Página {self.page_no()} / {{nb}}", align="C")

def generar_pdf_reporte_materia(datos):
    report_dir = "static/reports"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    pdf_path = os.path.join(report_dir, f"reporte_materia_{uuid.uuid4().hex}.pdf")

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_font("Arial", size=12)

    # Título
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Materia: {datos['materia']}", ln=True, align="C")
    pdf.ln(5)

    # Tabla
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(44, 62, 80)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(130, 10, "Alumno", border=1, align="C", fill=True)
    pdf.cell(50, 10, "Calificación", border=1, align="C", fill=True)
    pdf.ln()

    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)

    if datos["calificaciones"]:
        for reg in datos["calificaciones"]:
            nombre = reg.get("alumno", "N/A")
            calif = reg.get("calificacion", 0)
            pdf.cell(130, 10, nombre, border=1)
            pdf.cell(50, 10, str(calif), border=1, align="C")
            pdf.ln()
    else:
        pdf.cell(180, 10, "No hay alumnos registrados para esta materia.", ln=True, align="C")

    # Gráfica solo si hay datos
    nombres = [reg["alumno"] for reg in datos["calificaciones"]]
    califs = [reg["calificacion"] for reg in datos["calificaciones"]]

    if nombres and califs:
        plt.figure(figsize=(10, 5))
        plt.barh(nombres, califs, color='skyblue')
        plt.xlabel("Calificación")
        plt.title(f"Gráfica de Calificaciones - {datos['materia']}")
        plt.tight_layout()

        # Guardar imagen temporal
        img_path = f"static/reports/temp_{uuid.uuid4().hex}.png"
        plt.savefig(img_path)
        plt.close()

        # Añadir imagen al PDF
        pdf.add_page()
        pdf.image(img_path, x=10, y=30, w=pdf.w - 20)

        # Borrar imagen
        os.remove(img_path)

    pdf.output(pdf_path)
    return pdf_path


# ------------------------------------------------------------
# Route para descargar el reporte por alumno en PDF
# ------------------------------------------------------------


def generar_pdf_reporte_alumno(datos_alumno):
    """
    Genera un PDF con la información del alumno, historial académico y gráfica de pastel.
    """
    report_dir = "static/reports"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    pdf_path = os.path.join(report_dir, f"reporte_por_alumno.pdf")

    # 1. Crear la imagen de la gráfica
    labels = ['Aprobado', 'Reprobado', 'En curso']
    sizes = [
        datos_alumno.get("conteo_aprobadas", 0),
        datos_alumno.get("conteo_reprobadas", 0),
        datos_alumno.get("conteo_en_curso", 0)
    ]

    colors = ['#2ecc71', '#e74c3c', '#f1c40f']
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    ax.axis('equal')  # Para que el pastel sea circular

    image_filename = os.path.join(report_dir, f"{uuid.uuid4().hex}_avance.png")
    plt.savefig(image_filename, bbox_inches='tight')
    plt.close()

    # 2. Crear el PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    # Encabezado
    pdf.set_font("Arial", "B", 16)
    pdf.set_fill_color(41, 128, 185)  # Azul
    pdf.set_text_color(255)
    pdf.cell(0, 10, "Reporte por Alumno - SkyCode", ln=True, align="C", fill=True)
    pdf.ln(10)

    # Datos Generales
    pdf.set_text_color(0)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Datos del Alumno", ln=True)
    pdf.set_font("Arial", size=12)
    alumno = datos_alumno.get("alumno", {})
    pdf.cell(0, 10, f"Nombre: {alumno.get('nombre_completo', 'N/A')}", ln=True)
    pdf.cell(0, 10, f"Matrícula: {alumno.get('matricula', 'N/A')}", ln=True)
    pdf.cell(0, 10, f"Carrera: {alumno.get('carrera', 'N/A')}", ln=True)
    pdf.ln(5)

    # Tabla de Historial Académico
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Historial Académico", ln=True)
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(52, 73, 94)
    pdf.set_text_color(255)
    pdf.cell(100, 10, "Materia", 1, 0, 'C', True)
    pdf.cell(40, 10, "Calificación", 1, 0, 'C', True)
    pdf.cell(40, 10, "Estado", 1, 1, 'C', True)

    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0)
    for reg in datos_alumno.get("historial", []):
        pdf.cell(100, 10, reg.get("materia", "N/A"), 1)
        pdf.cell(40, 10, str(reg.get("calificacion", "N/A")), 1)
        pdf.cell(40, 10, reg.get("estado", "N/A"), 1, ln=True)

    pdf.ln(10)

    # Imagen de la gráfica de avance
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Avance en la Carrera", ln=True)
    pdf.image(image_filename, w=160)
    os.remove(image_filename)

    pdf.output(pdf_path)
    return pdf_path

