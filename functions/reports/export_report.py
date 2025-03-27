import os
from fpdf import FPDF

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
