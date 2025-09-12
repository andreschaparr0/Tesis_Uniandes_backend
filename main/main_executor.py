"""
Archivo principal que ejecuta la limpieza de datos.
"""

import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main.data_cleaner import DataCleaner


def main():
    """
    Función principal que ejecuta la limpieza de datos.
    """
    # Rutas de ejemplo
    cv = "exampleReal4"
    description = "CA_ejemplo1"
    
    cv_path = "src/images/" + cv + ".pdf"
    description_path = "src/descripciones/descripciones_ejemplos/" + description 

    print("LIMPIEZA DE DATOS")
    print("=" * 30)
    
    # Crear instancia del limpiador
    cleaner = DataCleaner()
    
    try:
        # Ejecutar limpieza
        cv_text, description_text = cleaner.process_both_files(cv_path, description_path)
        
        print(f"CV limpio: {len(cv_text)} caracteres")
        print(f"Descripción limpia: {len(description_text)} caracteres")
        return cv_text, description_text
        
    except Exception as e:
        print(f"Error: {e}")
        return None, None


if __name__ == "__main__":
    main()
