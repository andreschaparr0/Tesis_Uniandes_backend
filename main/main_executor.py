"""
Archivo principal que ejecuta la limpieza de datos.
"""

import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main.data_cleaner import DataCleaner
from main.data_structurer import DataStructurer
from main.recommendation_engine import RecommendationEngine


def main():
    """
    Función principal que ejecuta la limpieza de datos.
    """
    # Rutas de ejemplo
    
    cv = "exampleReal4"
    description = "CA_ejemplo1"
    
    cv_path = "src/images/" + cv + ".pdf"
    description_path = "src/descripciones/descripciones_ejemplos/" + description 

    print("SISTEMA DE RECOMENDACION")
    print("=" * 30)
    
    # Crear instancias
    cleaner = DataCleaner()
    structurer = DataStructurer()
    engine = RecommendationEngine()
    
    try:
        # FASE 1: LIMPIEZA
        print("FASE 1: LIMPIEZA")
        cv_text, description_text = cleaner.process_both_files(cv_path, description_path)
        print(f"CV limpio: {len(cv_text)} caracteres")
        print(f"Descripcion limpia: {len(description_text)} caracteres")
        
        # FASE 2: ESTRUCTURACION
        print("\nFASE 2: ESTRUCTURACION")
        cv_structured, job_structured = structurer.structure_both(cv_text, description_text)
        print(f"CV estructurado: {len(str(cv_structured))} caracteres")
        print(f"Descripcion estructurada: {len(str(job_structured))} caracteres")
        
        # FASE 3: RECOMENDACION
        print("\nFASE 3: RECOMENDACION")
        results = engine.generate_recommendation(cv_structured, job_structured)
        
        # Mostrar resultados usando el método de ComparatorMain
        engine.print_recommendation_results(cv_structured, job_structured, results)
        
        return results
        
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    main()
