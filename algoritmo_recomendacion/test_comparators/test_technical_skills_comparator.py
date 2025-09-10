"""
Test para el comparador de habilidades técnicas
"""

import sys
import os
# Agregar el directorio padre al path para importar el comparador
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from comparators.technical_skills_comparator import compare_technical_skills

def test_technical_skills_comparator():
    """
    Prueba escenarios simples - OPTIMIZADO: Una sola llamada a IA por comparación
    """
    print("\n=== TEST DE ESCENARIOS SIMPLES (OPTIMIZADO) ===\n")
    
    # Escenario 1: CV con habilidades que coinciden exactamente
    print("1. CV con habilidades que coinciden exactamente:")
    cv_skills = ["python", "sql", "java", "javascript"]
    job_skills = ["python", "sql", "java"]
    result1 = compare_technical_skills(cv_skills, job_skills)
    print(f"Puntaje: {result1['score']}")
    print(f"Coinciden: {len(result1['matched'])} habilidades")
    print(f"Faltan: {result1['missing']}")
    
    # Escenario 2: CV con habilidades parcialmente coincidentes
    print("\n2. CV con habilidades parcialmente coincidentes:")
    cv_skills = ["python", "sql", "nosql", "excel"]
    job_skills = ["python", "sql", "aws", "docker"]
    result2 = compare_technical_skills(cv_skills, job_skills)
    print(f"Puntaje: {result2['score']}")
    print(f"Coinciden: {len(result2['matched'])} habilidades")
    print(f"Faltan: {result2['missing']}")
    
    # Escenario 3: Sin habilidades requeridas
    print("\n3. Sin habilidades requeridas:")
    result3 = compare_technical_skills(["python", "sql"], [])
    print(f"Puntaje: {result3['score']}")
    print(f"Coinciden: {len(result3['matched'])} habilidades")
    print(f"Faltan: {result3['missing']}")
    
    # Escenario 4: CV sin habilidades técnicas
    print("\n4. CV sin habilidades técnicas:")
    result4 = compare_technical_skills([], ["python", "sql", "java"])
    print(f"Puntaje: {result4['score']}")
    print(f"Coinciden: {len(result4['matched'])} habilidades")
    print(f"Faltan: {result4['missing']}")
    
    # Escenario 5: Habilidades relacionadas (usando IA optimizada)
    print("\n5. Habilidades relacionadas (IA optimizada - UNA SOLA LLAMADA):")
    cv_skills = ["python", "sql", "nosql", "java", "javascript", "r", "excel"]
    job_skills = ["certificados aws", "certificados google cloud", "python", "sql"]
    result5 = compare_technical_skills(cv_skills, job_skills)
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
        "python",
        "sql", 
        "nosql",
        "java",
        "javascript",
        #"r",
        "excel"
    ]
    
    # Ejemplo de la descripción de trabajo
    job_skills = [
        "certificados aws",
        "certificados google cloud", 
        "conocimiento de normas y estándares internacionales de seguridad ti",
        "metodologías de análisis de riesgos de la información",
        "ejecución gestión y seguimiento de auditorías ti",
        "gestión de la seguridad y riesgos ti",
        "gestión de usuarios y roles",
        "conocimiento en proyectos de segregación de funciones",
        "conocimiento en seguridad en sap",
        "experiencia en seguridad de la información",
        "manejo de herramienta para modelamiento de procesos"
    ]
    
    result = compare_technical_skills(cv_skills, job_skills)
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
    #test_technical_skills_comparator()
    
    # Ejecutar test con ejemplos reales
    test_with_real_examples()
