"""
Test para el comparador de idiomas
"""

import json
import sys
import os

# Agregar el directorio padre al path para importar el comparador
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from comparators.languages_comparator import LanguagesComparator

def test_languages_comparator():
    """
    Prueba el comparador de idiomas con datos reales
    """
    print("=== TEST DEL COMPARADOR DE IDIOMAS ===\n")
    
    # Crear instancia del comparador
    comparator = LanguagesComparator()
    
    # Datos de prueba basados en los JSONs reales
    cv_languages = {
        "English": "B2",
        "Spanish": "Native"
    }
    
    job_languages = {
        "English": "B2 Minimum",
        "French": "B1"
    }
    
    print("Idiomas del CV:", cv_languages)
    print("Idiomas requeridos:", job_languages)
    print()
    
    # Realizar comparación
    result = comparator.compare_languages(cv_languages, job_languages)
    
    # Mostrar resultados
    print("=== RESULTADOS DE LA COMPARACIÓN ===")
    print(f"Porcentaje de coincidencia: {result['match_percentage']}%")
    print(f"Idiomas que coinciden: {result['matched_languages']}")
    print(f"Idiomas faltantes: {result['missing_languages']}")
    print(f"Total requeridos: {result['total_required']}")
    print(f"Total coincidentes: {result['total_matched']}")
    print()
    
    # Mostrar detalles de cada idioma
    print("=== DETALLES POR IDIOMA ===")
    for detail in result['language_details']:
        print(f"Idioma: {detail['language']}")
        print(f"  Nivel requerido: {detail['required_level']}")
        print(f"  Nivel del CV: {detail['cv_level']}")
        print(f"  Cumple requisito: {detail['meets_requirement']}")
        print(f"  Diferencia de nivel: {detail['level_difference']}")
        print()
    
    # Calcular puntaje
    score = comparator.get_language_score(result)
    print(f"Puntaje numérico: {score:.2f}")
    
    return result

def test_edge_cases():
    """
    Prueba casos extremos del comparador
    """
    print("\n=== TEST DE CASOS EXTREMOS ===")
    
    comparator = LanguagesComparator()
    
    # Caso 1: Sin idiomas requeridos
    print("\n1. Sin idiomas requeridos:")
    result1 = comparator.compare_languages({"English": "B2"}, {})
    print(f"Resultado: {result1['match_percentage']}%")
    
    # Caso 2: Sin idiomas en CV
    print("\n2. Sin idiomas en CV:")
    result2 = comparator.compare_languages({}, {"English": "B2"})
    print(f"Resultado: {result2['match_percentage']}%")
    
    # Caso 3: Niveles diferentes
    print("\n3. Niveles diferentes:")
    result3 = comparator.compare_languages(
        {"English": "B1"}, 
        {"English": "B2"}
    )
    print(f"Resultado: {result3['match_percentage']}%")
    print(f"Detalles: {result3['language_details']}")

if __name__ == "__main__":
    # Ejecutar test principal
    test_languages_comparator()
    
    # Ejecutar casos extremos
    test_edge_cases()
    
    print("\n=== FIN DE LOS TESTS ===")
