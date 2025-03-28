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
        self.set_font("Arial", "B", 16)
        self.set_fill_color(44, 62, 80)
        self.set_text_color(255, 255, 255)
        self.cell(200, 10, "Reporte Estadístico - SkyCode", ln=True, align='C', fill=True)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Página {self.page_no()} / {{nb}}", align='C')

def generar_pdf_reporte(datos_reporte):
    report_dir = "static/reports"
    report_path = os.path.join(report_dir, "reporte_estadistico.pdf")
    graph_path = os.path.join(report_dir, "grafica_estadistica.png")

    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    # Crear gráfica de barras
    carreras = list(datos_reporte.get("promedios_carreras", {}).keys())
    promedios = list(datos_reporte.get("promedios_carreras", {}).values())

    if carreras and promedios:
        plt.figure(figsize=(10, 5))
        plt.barh(carreras, promedios)
        plt.xlabel("Promedio")
        plt.title("Promedio por Carrera")
        plt.tight_layout()
        plt.savefig(graph_path)
        plt.close()

    # Generar PDF
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Totales
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Total de Alumnos: {datos_reporte.get('total_alumnos', 0)}", ln=True, align='C')
    pdf.cell(0, 10, f"Total de Egresados: {datos_reporte.get('total_egresados', 0)}", ln=True, align='C')

    pdf.ln(10)

    # Tabla de promedios
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Promedio por Carrera", ln=True, align='C')

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(44, 62, 80)
    pdf.set_text_color(255, 255, 255)

    pdf.cell(90, 10, "Carrera", border=1, align='C', fill=True)
    pdf.cell(50, 10, "Promedio", border=1, align='C', fill=True)
    pdf.cell(50, 10, "Egresados", border=1, align='C', fill=True)
    pdf.ln()

    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)

    for carrera, promedio in datos_reporte.get("promedios_carreras", {}).items():
        pdf.cell(90, 10, carrera, border=1, align='C')
        pdf.cell(50, 10, f"{round(promedio, 2)}", border=1, align='C')
        pdf.cell(50, 10, "N/A", border=1, align='C')
        pdf.ln()

    # Insertar gráfica (si se generó)
    if os.path.exists(graph_path):
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Gráfica de Promedios por Carrera", ln=True, align='C')
        pdf.image(graph_path, x=30, w=150)

    pdf.output(report_path)
    return report_path


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


# ------------------------------------------------------------
# Route para descargar el reporte por evaluacion en PDF
# ------------------------------------------------------------
class PDFEvaluacion(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.set_fill_color(44, 62, 80)  # Azul base
        self.set_text_color(255, 255, 255)  # Texto blanco
        self.cell(0, 10, "Reporte por Evaluación - SkyCode", ln=True, align='C', fill=True)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Página {self.page_no()} / {{nb}}", align='C')



def generar_pdf_reporte_evaluacion(reporte):
    path_dir = "static/reports"
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)

    path_pdf = os.path.join(path_dir, "reporte_evaluacion.pdf")

    pdf = PDFEvaluacion()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    if not reporte:
        pdf.cell(0, 10, "No hay datos disponibles.", ln=True, align='C')
    else:
        # Gráfico de barras: Promedio por materia
        materias = []
        promedios = []

        for grupo in reporte:
            materia = grupo["materia"]
            alumnos = grupo["alumnos"]
            materias.append(materia)

            if alumnos:
                promedio = sum([a["calificacion"] for a in alumnos]) / len(alumnos)
            else:
                promedio = 0

            promedios.append(promedio)

        # 🎯 Guardar gráfico
        grafica_path = os.path.join(path_dir, "grafica_evaluacion.png")
        plt.figure(figsize=(10, 5))
        plt.barh(materias, promedios)
        plt.xlabel("Promedio")
        plt.title("Promedio por Materia")
        plt.tight_layout()
        plt.savefig(grafica_path)
        plt.close()

        # 🧾 Sección de tabla por materia
        for grupo in reporte:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, f"Materia: {grupo['materia']}", ln=True)
            pdf.set_font("Arial", size=11)

            pdf.set_fill_color(220, 220, 220)
            pdf.cell(100, 8, "Alumno", 1, 0, 'C', fill=True)
            pdf.cell(40, 8, "Calificación", 1, 1, 'C', fill=True)

            for alumno in grupo["alumnos"]:
                pdf.cell(100, 8, alumno["alumno"], 1)
                pdf.cell(40, 8, str(alumno["calificacion"]), 1)
                pdf.ln()

            pdf.ln(5)

        # Agregar la gráfica como imagen
        if os.path.exists(grafica_path):
            pdf.add_page()
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "Gráfica de Promedios por Materia", ln=True, align="C")
            pdf.image(grafica_path, x=30, w=150)

    pdf.output(path_pdf)
    return path_pdf

# ------------------------------------------------------------
# Route para descargar el reporte por grupo en PDF
# ------------------------------------------------------------

class PDFGrupo(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.set_fill_color(44, 62, 80)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, "Reporte por Grupo - SkyCode", 0, 1, 'C', fill=True)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Página {self.page_no()} / {{nb}}", align='C')

def generar_pdf_reporte_grupo(datos):
    path_dir = "static/reports"
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)

    path_pdf = os.path.join(path_dir, "reporte_grupo.pdf")

    pdf = PDFGrupo()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    if not datos:
        pdf.cell(0, 10, "No hay datos disponibles.", ln=True, align='C')
    else:
        for grupo in datos:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, f"Carrera: {grupo['carrera']} ({grupo['cantidad']} alumnos)", ln=True)
            pdf.set_font("Arial", size=11)
            pdf.cell(100, 8, "Alumno", 1)
            pdf.cell(60, 8, "Estado", 1)
            pdf.ln()
            for alumno in grupo["alumnos"]:
                pdf.cell(100, 8, alumno["nombre"], 1)
                pdf.cell(60, 8, alumno["estado"], 1)
                pdf.ln()
            pdf.ln(5)

    # 🔸 Agregar gráfica si existe
    graph_path = os.path.join("static/reports", "grafica_grupo.png")
    if os.path.exists(graph_path):
        pdf.add_page()
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Gráfica de Alumnos por Grupo", ln=True, align="C")
        pdf.image(graph_path, x=30, w=150)

    pdf.output(path_pdf)
    return path_pdf

# ------------------------------------------------------------
# Route para descargar el reporte por carrera en PDF
# ------------------------------------------------------------

class PDFCarrera(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.set_fill_color(44, 62, 80)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, "Reporte por Carrera - SkyCode", ln=True, align='C', fill=True)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Página {self.page_no()} / {{nb}}", align='C')

def generar_pdf_reporte_carrera(data):
    report_dir = "static/reports"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    pdf = PDFCarrera()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    if not data:
        pdf.cell(0, 10, "No hay datos disponibles para mostrar.", ln=True, align='C')
    else:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(80, 10, "Carrera", 1)
        pdf.cell(40, 10, "Alumnos", 1)
        pdf.cell(40, 10, "Promedio", 1)
        pdf.ln()

        pdf.set_font("Arial", size=12)
        for carrera in data:
            pdf.cell(80, 10, carrera["carrera"], 1)
            pdf.cell(40, 10, str(carrera["total_alumnos"]), 1)
            pdf.cell(40, 10, str(carrera["promedio"]), 1)
            pdf.ln()

        # Gráfico de barras
        nombres = [c["carrera"] for c in data]
        promedios = [c["promedio"] for c in data]

        plt.figure(figsize=(10, 5))
        plt.barh(nombres, promedios)
        plt.title("Promedio por Carrera")
        plt.xlabel("Promedio")
        plt.tight_layout()
        grafica_path = os.path.join(report_dir, "grafica_carrera.png")
        plt.savefig(grafica_path)
        plt.close()

        if os.path.exists(grafica_path):
            pdf.add_page()
            pdf.image(grafica_path, x=20, w=170)

    pdf_path = os.path.join(report_dir, "reporte_por_carrera.pdf")
    pdf.output(pdf_path)
    return pdf_path
