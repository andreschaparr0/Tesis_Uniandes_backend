import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """
    Extrae y concatena el texto de todas las páginas de un PDF.
    Args:
        pdf_path (str): Ruta al archivo PDF.
    Returns:
        str: Texto extraído del PDF.
    """
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
            text += "\n"
    return text
