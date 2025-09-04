from .job_description_extractor import JobDescriptionExtractor
import json
import os
from ..limpieza.limpieza import clean_text
# Variables Globales
txt_path = "src/descripciones/descripciones_ejemplos/CA_Ejemplo1"
nombreJson = "CA_Ejemplo1.json"

def test_job_description_extraction():
    """
    Prueba la extracción de descripciones de trabajo usando LangChain.
    """
    
    # Verificar que existe el archivo .env
    if not os.path.exists(".env"):
        print("Crea un archivo .env con tu API key:")
        print("API_TOKEN=tu_api_key_aqui")
        return
    
    try:
        # Crear el extractor
        extractor = JobDescriptionExtractor()
        print("Extractor de descripciones de trabajo creado exitosamente")
        
        if not os.path.exists(txt_path):
            print("No se encontró archivo de descripción de trabajo.")
            print("Asegúrate de tener el archivo en la carpeta 'src/descripciones/'")
            return
        
        print(f"Procesando descripción de trabajo: {txt_path}")
        
        try:
            # Leer el archivo de texto
            with open(txt_path, 'r', encoding='utf-8') as f:
                raw_text = f.read()
            
            print(f"Texto leído ({len(raw_text)} caracteres)")

            print("PRUEBA: EXTRACCIÓN DE DESCRIPCIÓN DE TRABAJO")
            
            #Limpieza de texto
            raw_text = clean_text(raw_text)
            # Extraer toda la descripción
            job_structure = extractor.extract_full_job_description(raw_text)
            
            # Guardar en JSON
            output_path = "src/estructuracion_Descripcion/DescripcionesEjemplos/" + nombreJson
            extractor.save_to_json(job_structure, output_path)
            print(f"✅ Archivo guardado en: {output_path}")
            
        except Exception as e:
            print(f"❌ Error procesando descripción: {e}")
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        print("Verifica que tu API key esté configurada correctamente en el archivo .env")

if __name__ == "__main__":
    test_job_description_extraction()