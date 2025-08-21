from cv_structured_extractor import CVStructuredExtractor, extract_cv_to_json
import json
import os
import re

extractor = CVStructuredExtractor()

# Procesar PDF de ejemplo si existe
pdf_path = "../images/example.pdf"
if os.path.exists(pdf_path):
    try:
        cv_data = extractor.extract_from_pdf(pdf_path)
        print("CV estructurado:")
        print(json.dumps(cv_data, ensure_ascii=False, indent=2))
        
        # Guardar en JSON
        output_path = "cv_structured.json"
        extractor.save_to_json(cv_data, output_path)
        
    except Exception as e:
        print(f"Error: {e}")
else:
    print("No se encontró PDF de ejemplo. Asegúrate de tener un PDF en la carpeta 'images'.")
