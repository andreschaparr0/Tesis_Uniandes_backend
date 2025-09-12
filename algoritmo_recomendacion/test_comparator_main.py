"""
Test simple para comparator_main.py
Prueba la funcionalidad con los JSONs específicos.
"""

import sys
import os

# Agregar el directorio actual al path para importar comparator_main
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from comparator_main import ComparatorMain


def test_comparator_main():
    """
    Prueba simple del comparator_main con los JSONs específicos.
    """
    print("=== TEST DE COMPARATOR_MAIN ===")
    
    # Crear instancia del comparador
    comparator = ComparatorMain()
    
    # Rutas a los archivos específicos
    cv = "exampleReal4"
    job = "CA_Ejemplo1" 
    cv_file = "src/estructuracion_CV/CvEjemplos/" + cv + ".json"
    job_file = "src/estructuracion_Descripcion/DescripcionesEjemplos/" + job + ".json"
    
    print(f"CV: {cv_file}")
    print(f"Descripción: {job_file}")
    
    # Ejecutar todas las comparaciones y obtener datos
    
    data = comparator.run_comparisons(cv_file, job_file)
    
    if data:
        cv_data, job_data, results = data
        
        # Imprimir resultados
        comparator.print_comparison_results(cv_data, job_data, results)
        
        print("\n=== TEST COMPLETADO ===")
        print(f"Se ejecutaron {len(results)} comparaciones")
    else:
        print("\n=== ERROR EN EL TEST ===")
        print("No se pudieron ejecutar las comparaciones")


if __name__ == "__main__":
    test_comparator_main()
