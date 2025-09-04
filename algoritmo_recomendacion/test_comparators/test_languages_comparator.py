"""
Test para el comparador de idiomas
"""

import json
import sys
import os
print("=== TEST DEL COMPARADOR DE IDIOMAS CON DATOS REALES ===")
# Agregar el directorio padre al path para importar el comparador
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from comparators.languages_comparator import compare_languages, get_language_score

def load_test_data():
    """
    Carga los datos de prueba desde los JSONs reales
    """
    # Ruta a los archivos JSON
    cv_path = "../../src/estructuracion_CV/CvEjemplos/exampleReal.json"
    job_path = "../../src/estructuracion_Descripcion/DescripcionesEjemplos/CA_Ejemplo1.json"
    
    try:
        # Cargar CV
        with open(cv_path, 'r', encoding='utf-8') as f:
            cv_data = json.load(f)
        
        # Cargar descripción de trabajo
        with open(job_path, 'r', encoding='utf-8') as f:
            job_data = json.load(f)
        
        return cv_data, job_data
    except FileNotFoundError as e:
        print(f"Error: No se encontró el archivo {e}")
        return None, None
    except json.JSONDecodeError as e:
        print(f"Error al parsear JSON: {e}")
        return None, None

def test_languages_comparator():
    """
    Prueba el comparador de idiomas con datos reales de los JSONs
    """
    print("=== TEST DEL COMPARADOR DE IDIOMAS CON DATOS REALES ===\n")
    
    # Cargar datos de prueba
    cv_data, job_data = load_test_data()
    
    if not cv_data or not job_data:
        print("No se pudieron cargar los datos de prueba")
        return
    
    # Extraer idiomas del CV
    cv_languages = cv_data.get("languages", {})
    
    # Extraer idiomas requeridos del trabajo
    job_languages = {}
    qualifications = job_data.get("qualifications", {})
    if qualifications:
        requirements = qualifications.get("requirements", {})
        if requirements:
            job_languages = requirements.get("languages", {})
    
    print("Idiomas del CV:", cv_languages)
    print("Idiomas requeridos:", job_languages)
    print()
    
    # Realizar comparación
    result = compare_languages(cv_languages, job_languages)
    
    # Mostrar resultados
    print("=== RESULTADOS DE LA COMPARACIÓN ===")
    print(f"Puntaje: {result['score']}")
    print(f"Idiomas que coinciden: {result['matched']}")
    print(f"Idiomas faltantes: {result['missing']}")
    print()
    
    # Calcular puntaje final
    score = get_language_score(result)
    print(f"Puntaje final: {score:.2f}")
    
    return result

def test_simple_scenarios():
    """
    Prueba escenarios simples
    """
    print("\n=== TEST DE ESCENARIOS SIMPLES ===\n")
    
    # Escenario 1: CV con nivel superior
    print("1. CV con nivel superior:")
    cv_lang = {"English": "C1"}
    job_lang = {"English": "B2"}
    result1 = compare_languages(cv_lang, job_lang)
    print(f"Puntaje: {result1['score']}")
    
    # Escenario 2: CV con nivel inferior
    print("\n2. CV con nivel inferior:")
    cv_lang = {"English": "B1"}
    job_lang = {"English": "B2"}
    result2 = compare_languages(cv_lang, job_lang)
    print(f"Puntaje: {result2['score']}")
    
    # Escenario 3: Sin idiomas requeridos
    print("\n3. Sin idiomas requeridos:")
    result3 = compare_languages({"English": "B2"}, {})
    print(f"Puntaje: {result3['score']}")

if __name__ == "__main__":
    # Ejecutar test principal con datos reales\
    print("=== TEST DEL COMPARADOR DE IDIOMAS CON DATOS REALES ===")
    test_languages_comparator()
    
    # Ejecutar escenarios simples
    test_simple_scenarios()
    
    print("\n=== FIN DE LOS TESTS ===")
