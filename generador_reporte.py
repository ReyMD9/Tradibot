import sqlite3
import pandas as pd
from fpdf import FPDF

class PDFReporte(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 15)
        self.cell(0, 10, "Reporte de Auditoria - Tradibot", 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", 'I', 8)
        self.cell(0, 10, f"Pagina {self.page_no()}", 0, 0, 'C')

def generar_pdf_auditoria(archivo_pdf="reporte_auditoria.pdf"):
    # 1. Extraer datos de la base de datos
    conn = sqlite3.connect("trade_history.db")
    df = pd.read_sql_query("SELECT * FROM trades", conn)
    conn.close()

    # 2. Iniciar PDF
    pdf = PDFReporte()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    # 3. Resumen Ejecutivo
    pdf.cell(200, 10, f"Total de operaciones registradas: {len(df)}", ln=True)
    pdf.ln(10)

    # 4. Tabla de Datos (Formato Contable)
    # Encabezados
    pdf.set_font("Arial", 'B', 10)
    col_widths = [40, 30, 20, 30, 30]
    headers = ["Fecha", "Simbolo", "Cant", "Precio", "Tipo"]
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 10, h, border=1)
    pdf.ln()

    # Contenido
    pdf.set_font("Arial", size=9)
    for _, row in df.iterrows():
        fecha = str(row['fecha'])[:19] # Formato corto
        pdf.cell(col_widths[0], 10, fecha, border=1)
        pdf.cell(col_widths[1], 10, str(row['simbolo']), border=1)
        pdf.cell(col_widths[2], 10, str(row['cantidad']), border=1)
        pdf.cell(col_widths[3], 10, f"${row['precio_entrada']:.2f}", border=1)
        pdf.cell(col_widths[4], 10, str(row['tipo']), border=1)
        pdf.ln()

    pdf.output(archivo_pdf)
    print(f"✅ Reporte generado exitosamente: {archivo_pdf}")

if __name__ == "__main__":
    generar_pdf_auditoria()