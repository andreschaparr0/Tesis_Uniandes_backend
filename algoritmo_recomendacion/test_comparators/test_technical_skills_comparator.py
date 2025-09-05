"""
Test para el comparador de habilidades técnicas
"""

import sys
import os
# Agregar el directorio padre al path para importar el comparador
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from comparators.technical_skills_comparator import compare_technical_skills, get_technical_skills_score

def test_technical_skills_comparator():
    """
    Prueba el comparador de habilidades técnicas con datos de ejemplo
    """
    print("=== TEST DEL COMPARADOR DE HABILIDADES TÉCNICAS ===\n")
    
    # Datos de ejemplo basados en los JSONs reales
    cv_skills = [
        "Python",
        "SQL",
        "JavaScript",
        "GitHub",
        "Excel"
    ]
    
    job_skills = [
        "Conocimiento de normas y estándares internacionales de seguridad TI",
        "Conocimiento de metodologías de análisis de riesgos de la información",
        "Gestión de usuarios y roles",
        "Conocimiento en seguridad en SAP",
        "Python"
    ]
    
    print("Habilidades del CV:", cv_skills)
    print("Habilidades requeridas:", job_skills)
    print()
    
    # Realizar comparación
    result = compare_technical_skills(cv_skills, job_skills)
    
    # Mostrar resultados
    print("=== RESULTADOS DE LA COMPARACIÓN ===")
    print(f"Puntaje: {result['score']}")
    print(f"Habilidades que coinciden: {result['matched']}")
    print(f"Habilidades faltantes: {result['missing']}")
    print()
    
    # Calcular puntaje final
    score = get_technical_skills_score(result)
    print(f"Puntaje final: {score:.2f}")
    
    return result

def test_simple_scenarios():
    """
    Prueba escenarios simples
    """
    print("\n=== TEST DE ESCENARIOS SIMPLES ===\n")
    
    # Escenario 1: Habilidad exacta
    print("1. Habilidad exacta:")
    cv_skills = ["python"]
    job_skills = ["python"]
    result1 = compare_technical_skills(cv_skills, job_skills)
    print(f"Puntaje: {result1['score']}")
    print(f"Coinciden: {result1['matched']}")
    print(f"Faltan: {result1['missing']}")
    
    # Escenario 2: Habilidades diferentes
    print("\n2. Habilidades diferentes:")
    cv_skills = ["Java", "C++"]
    job_skills = ["Python", "JavaScript"]
    result2 = compare_technical_skills(cv_skills, job_skills)
    print(f"Puntaje: {result2['score']}")
    print(f"Coinciden: {result2['matched']}")
    print(f"Faltan: {result2['missing']}")
    
    # Escenario 3: Sin habilidades requeridas
    print("\n3. Sin habilidades requeridas:")
    result3 = compare_technical_skills(["Python", "SQL"], [])
    print(f"Puntaje: {result3['score']}")
    print(f"Coinciden: {result3['matched']}")
    print(f"Faltan: {result3['missing']}")
    
    # Escenario 4: Múltiples habilidades
    print("\n4. Múltiples habilidades:")
    cv_skills = ["Python", "SQL", "JavaScript", "GitHub"]
    job_skills = ["Python", "SQL", "Machine Learning"]
    result4 = compare_technical_skills(cv_skills, job_skills)
    print(f"Puntaje: {result4['score']}")
    print(f"Coinciden: {result4['matched']}")
    print(f"Faltan: {result4['missing']}")
    
    # Escenario 5: Habilidades similares
    print("\n5. Habilidades similares:")
    cv_skills = ["Python Programming"]
    job_skills = ["Python"]
    result5 = compare_technical_skills(cv_skills, job_skills)
    print(f"Puntaje: {result5['score']}")
    print(f"Coinciden: {result5['matched']}")
    print(f"Faltan: {result5['missing']}")
    
    # Escenario 6: Habilidades relacionadas
    print("\n6. Habilidades relacionadas:")
    cv_skills = ["Machine Learning", "Data Science"]
    job_skills = ["Artificial Intelligence", "Big Data"]
    result6 = compare_technical_skills(cv_skills, job_skills)
    print(f"Puntaje: {result6['score']}")
    print(f"Coinciden: {result6['matched']}")
    print(f"Faltan: {result6['missing']}")

if __name__ == "__main__":
    # Ejecutar test principal
    test_technical_skills_comparator()
    
    # Ejecutar escenarios simples
    test_simple_scenarios()
    
    print("\n=== FIN DE LOS TESTS ===")
