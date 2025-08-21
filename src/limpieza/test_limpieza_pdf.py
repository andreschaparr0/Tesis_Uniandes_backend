from pdf_text_extractor import extract_text_from_pdf
from limpieza import clean_text
import os


print("Prueba de extracción y limpieza de texto de PDF y de texto plano\n")

# 1. Prueba con texto de ejemplo
ejemplo = """
John Doe
Software Engineer
Experience: Developed web applications using Python and JavaScript. 2020-2023
Education: BSc in Computer Science
Skills: Python, JavaScript, Machine Learning, Data Analysis
"""
print("--- Texto de ejemplo ---\n")
print(ejemplo)
print("\n--- Texto limpio (ejemplo) ---\n")
print(clean_text(ejemplo))

# 2. Prueba con PDF
pdf_path = os.path.join("../images", "example.pdf")

if pdf_path:
    try:
        texto = extract_text_from_pdf(pdf_path)
        print("\n--- Texto extraído del PDF ---\n")
        print(texto)
        print("\n--- Texto limpio (PDF) ---\n")
        print(clean_text(texto))
    except Exception as e:
        print(f"Error al procesar el PDF: {e}")
else:
    print("No se ingresó ruta de PDF. Solo se probó con texto de ejemplo.") 