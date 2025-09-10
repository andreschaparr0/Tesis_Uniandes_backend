from .cv_simple_extractor import SimpleCVExtractor
from ..limpieza.limpieza import clean_text
import json
import os

#Variables Globales
pdf_path = "src/images/exampleReal4.pdf"
nombreJson = "exampleReal4.json"

def test_langchain_extraction():
    """
    Prueba la extracción usando LangChain con todas sus funcionalidades.
    Solo usa el PDF real, no texto de ejemplo.
    """
    
    # Verificar que existe el archivo .env
    if not os.path.exists(".env"):
        print("Crea un archivo .env con tu API key:")
        print("API_TOKEN=tu_api_key_aqui")
        return
    
    try:
        # Crear el extractor
        extractor = SimpleCVExtractor()
        print("Extractor con LangChain creado exitosamente")
        
        
        if not os.path.exists(pdf_path):
            print(" No se encontró PDF de ejemplo.")
            print("   Asegúrate de tener un PDF en la carpeta 'src/images/'")
            return
        
        print(f"Procesando PDF real: {pdf_path}")
        
        try:
            # Importar aquí para evitar errores si no existe
            from ..limpieza.pdf_text_extractor import extract_text_from_pdf
            
            # Extraer texto del PDF
            raw_text = extract_text_from_pdf(pdf_path)
            print(f"Texto extraído del PDF ({len(raw_text)} caracteres)")
            raw_text = clean_text(raw_text)
            #print(raw_text)
            print("PRUEBA: LANGCHAIN")

            cv_structure = extractor.extract_full_cv_simple(raw_text)
            # Guardar en JSON
            
            output_path = "src/estructuracion_CV/CvEjemplos/" + nombreJson
            extractor.save_to_json(cv_structure, output_path)
            print(f"Archivo guardado en: {output_path}")
            
        except Exception as e:
            print(f"rror procesando PDF: {e}")
        
\
    except Exception as e:
        print(f"Error general: {e}")
        print("Verifica que tu API key esté configurada correctamente en el archivo .env")

if __name__ == "__main__":
    test_langchain_extraction()
