"""
Test para el comparador de idiomas
"""

import sys
import os
# Agregar el directorio padre al path para importar el comparador
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from comparators.languages_comparator import compare_languages

def test_languages_comparator():
    """
    Prueba escenarios simples
    """
    print("\n=== TEST DE ESCENARIOS SIMPLES ===\n")
    
    # Escenario 1: CV con nivel superior al requerido
    print("1. CV con nivel superior al requerido:")
    cv_lang = {"English": "C1"}
    job_lang = {"English": "B2"}
    result1 = compare_languages(cv_lang, job_lang)
    print(f"Puntaje: {result1['score']}")
    print(f"Razón: {result1['reason']}")
    
    # Escenario 2: CV con nivel inferior al requerido
    print("\n2. CV con nivel inferior al requerido:")
    cv_lang = {"English": "B1"}
    job_lang = {"English": "B2"}
    result2 = compare_languages(cv_lang, job_lang)
    print(f"Puntaje: {result2['score']}")
    print(f"Razón: {result2['reason']}")
    
    # Escenario 3: Sin idiomas requeridos
    print("\n3. Sin idiomas requeridos:")
    result3 = compare_languages({"English": "B2"}, {})
    print(f"Puntaje: {result3['score']}")
    print(f"Razón: {result3['reason']}")
    
    # Escenario 4: Múltiples idiomas
    print("\n4. Múltiples idiomas:")
    cv_lang = {"English": "B2", "Spanish": "Native", "French": "A1"}
    job_lang = {"English": "B2", "German": "B1"}
    result4 = compare_languages(cv_lang, job_lang)
    print(f"Puntaje: {result4['score']}")
    print(f"Razón: {result4['reason']}")

if __name__ == "__main__":
    # Ejecutar escenarios simples
    test_languages_comparator()

