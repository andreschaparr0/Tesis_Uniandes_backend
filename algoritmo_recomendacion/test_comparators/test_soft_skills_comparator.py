"""
Test para el comparador de habilidades blandas
"""

import sys
import os
# Agregar el directorio padre al path para importar el comparador
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from comparators.soft_skills_comparator import compare_soft_skills

def test_soft_skills_comparator():
    """
    Prueba escenarios simples - OPTIMIZADO: Una sola llamada a IA por comparación
    """
    print("\n=== TEST DE ESCENARIOS SIMPLES (OPTIMIZADO) ===\n")
    
    # Escenario 1: CV con habilidades que coinciden exactamente
    print("1. CV con habilidades que coinciden exactamente:")
    cv_skills = ["teamwork", "leadership", "problem solving", "communication"]
    job_skills = ["teamwork", "leadership", "problem solving"]
    result1 = compare_soft_skills(cv_skills, job_skills)
    print(f"Puntaje: {result1['score']}")
    print(f"Coinciden: {len(result1['matched'])} habilidades")
    print(f"Faltan: {result1['missing']}")
    
    # Escenario 2: CV con habilidades parcialmente coincidentes
    print("\n2. CV con habilidades parcialmente coincidentes:")
    cv_skills = ["teamwork", "leadership", "adaptability", "creativity"]
    job_skills = ["teamwork", "leadership", "time management", "stress management"]
    result2 = compare_soft_skills(cv_skills, job_skills)
    print(f"Puntaje: {result2['score']}")
    print(f"Coinciden: {len(result2['matched'])} habilidades")
    print(f"Faltan: {result2['missing']}")
    
    # Escenario 3: Sin habilidades requeridas
    print("\n3. Sin habilidades requeridas:")
    result3 = compare_soft_skills(["teamwork", "leadership"], [])
    print(f"Puntaje: {result3['score']}")
    print(f"Coinciden: {len(result3['matched'])} habilidades")
    print(f"Faltan: {result3['missing']}")
    
    # Escenario 4: CV sin habilidades blandas
    print("\n4. CV sin habilidades blandas:")
    result4 = compare_soft_skills([], ["teamwork", "leadership", "communication"])
    print(f"Puntaje: {result4['score']}")
    print(f"Coinciden: {len(result4['matched'])} habilidades")
    print(f"Faltan: {result4['missing']}")
    
    # Escenario 5: Habilidades relacionadas (usando IA optimizada)
    print("\n5. Habilidades relacionadas (IA optimizada - UNA SOLA LLAMADA):")
    cv_skills = ["teamwork", "leadership", "problem solving", "critical thinking", "adaptability", "proactivity", "effective communication"]
    job_skills = ["collaboration", "management skills", "analytical thinking", "flexibility"]
    result5 = compare_soft_skills(cv_skills, job_skills)
    print(f"Puntaje: {result5['score']}")
    print(f"Coinciden: {len(result5['matched'])} habilidades")
    print(f"Faltan: {result5['missing']}")
    
    # Mostrar detalles de las coincidencias
    if result5['matched']:
        print("\nDetalles de coincidencias:")
        for match in result5['matched']:
            print(f"  CV: {match['cv_skill']} -> Requerido: {match['required_skill']} (Score: {match['score']})")
    
def test_with_real_examples():
    """
    Prueba con ejemplos reales del proyecto - OPTIMIZADO: Una sola llamada a IA
    """
    print("\n=== TEST CON EJEMPLOS REALES (OPTIMIZADO) ===\n")
    
    # Ejemplo del CV real
    cv_skills = [
        "teamwork",
        "leadership", 
        "problem solving",
        "critical thinking",
        "adaptability",
        "proactivity",
        "effective communication"
    ]
    
    # Ejemplo de la descripción de trabajo (vacío en el ejemplo, pero podemos simular)
    job_skills = [
        "collaboration",
        "leadership",
        "analytical thinking",
        "adaptability",
        "communication skills",
        "initiative",
        "team management"
    ]
    
    result = compare_soft_skills(cv_skills, job_skills)
    print(f"Puntaje total: {result['score']}")
    print(f"Habilidades coincidentes: {len(result['matched'])}")
    print(f"Habilidades faltantes: {len(result['missing'])}")
    
    if result['matched']:
        print("\nHabilidades que coinciden:")
        for match in result['matched']:
            print(f"  ✓ {match['cv_skill']} -> {match['required_skill']} (Score: {match['score']})")
    
    if result['missing']:
        print("\nHabilidades faltantes:")
        for skill in result['missing']:
            print(f"  ✗ {skill}")

def test_soft_skills_synonyms():
    """
    Prueba específica para sinónimos y habilidades relacionadas
    """
    print("\n=== TEST DE SINÓNIMOS Y HABILIDADES RELACIONADAS ===\n")
    
    cv_skills = [
        "teamwork",
        "leadership", 
        "problem solving",
        "critical thinking",
        "adaptability",
        "proactivity",
        "effective communication"
    ]
    
    # Habilidades con sinónimos y variaciones
    job_skills = [
        "collaboration",  # sinónimo de teamwork
        "management",     # relacionado con leadership
        "analytical skills",  # relacionado con critical thinking
        "flexibility",    # sinónimo de adaptability
        "initiative",     # relacionado con proactivity
        "interpersonal skills",  # relacionado con communication
        "decision making"  # relacionado con problem solving
    ]
    
    result = compare_soft_skills(cv_skills, job_skills)
    print(f"Puntaje total: {result['score']}")
    print(f"Habilidades coincidentes: {len(result['matched'])}")
    print(f"Habilidades faltantes: {len(result['missing'])}")
    
    if result['matched']:
        print("\nHabilidades que coinciden:")
        for match in result['matched']:
            print(f"  ✓ {match['cv_skill']} -> {match['required_skill']} (Score: {match['score']})")
    
    if result['missing']:
        print("\nHabilidades faltantes:")
        for skill in result['missing']:
            print(f"  ✗ {skill}")

if __name__ == "__main__":
    # Ejecutar escenarios simples
    test_soft_skills_comparator()
    
    # Ejecutar test con ejemplos reales
    test_with_real_examples()
    
    # Ejecutar test de sinónimos
    test_soft_skills_synonyms()
