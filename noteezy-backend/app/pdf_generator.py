from fpdf import FPDF
import os

def generate_pdf(content, username):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in content.splitlines():
        pdf.multi_cell(0, 10, line)
    filename = f"noteezy_{username.replace('@', '_')}.pdf"
    path = os.path.join("logs", filename)
    pdf.output(path)
    return path