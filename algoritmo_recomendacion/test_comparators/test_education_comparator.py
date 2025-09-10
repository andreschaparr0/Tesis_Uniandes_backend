"""
Test para el comparador de educación
"""

import sys
import os
# Agregar el directorio padre al path para importar el comparador
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from comparators.education_comparator import compare_education

def test_education_comparator():
    """
    Prueba escenarios simples - OPTIMIZADO: Una sola llamada a IA por comparación
    """
    print("\n=== TEST DE ESCENARIOS SIMPLES (OPTIMIZADO) ===\n")
    
    # Escenario 1: CV con educación que coincide exactamente
    print("1. CV con educación que coincide exactamente:")
    cv_education = [
        {
            "degree": "ingeniería de sistemas y computación",
            "institution": "universidad de los andes",
            "year": "2023",
            "field": "ingeniería de sistemas"
        }
    ]
    job_education = "egresado de la carreras técnicas o universitarias de ingeniería de sistemas computación ingeniería informática o afines"
    result1 = compare_education(cv_education, job_education)
    print(f"Puntaje: {result1['score']}")
    print(f"Coinciden: {len(result1['matched'])} educaciones")
    print(f"Faltan: {result1['missing']}")
    print(f"Razón: {result1['reason']}")
    
    # Escenario 2: CV con educación parcialmente coincidente
    print("\n2. CV con educación parcialmente coincidente:")
    cv_education = [
        {
            "degree": "técnico en programación",
            "institution": "sena",
            "year": "2022",
            "field": "programación"
        }
    ]
    job_education = "egresado de la carreras técnicas o universitarias de ingeniería de sistemas computación ingeniería informática o afines"
    result2 = compare_education(cv_education, job_education)
    print(f"Puntaje: {result2['score']}")
    print(f"Coinciden: {len(result2['matched'])} educaciones")
    print(f"Faltan: {result2['missing']}")
    print(f"Razón: {result2['reason']}")
    
    # Escenario 3: Sin requisitos educativos
    print("\n3. Sin requisitos educativos:")
    result3 = compare_education(cv_education, "")
    print(f"Puntaje: {result3['score']}")
    print(f"Coinciden: {len(result3['matched'])} educaciones")
    print(f"Faltan: {result3['missing']}")
    print(f"Razón: {result3['reason']}")
    
    # Escenario 4: CV sin información educativa
    print("\n4. CV sin información educativa:")
    result4 = compare_education([], job_education)
    print(f"Puntaje: {result4['score']}")
    print(f"Coinciden: {len(result4['matched'])} educaciones")
    print(f"Faltan: {result4['missing']}")
    print(f"Razón: {result4['reason']}")
    
    # Escenario 5: Múltiples educaciones (usando IA optimizada)
    print("\n5. Múltiples educaciones (IA optimizada - UNA SOLA LLAMADA):")
    cv_education = [
        {
            "degree": "ingeniería de sistemas y computación",
            "institution": "universidad de los andes",
            "year": "2023",
            "field": "ingeniería de sistemas"
        },
        {
            "degree": "bachiller académico",
            "institution": "colegio bilingue lisa meitner",
            "year": "2018",
            "field": "educación secundaria"
        }
    ]
    job_education = "egresado de la carreras técnicas o universitarias de ingeniería de sistemas computación ingeniería informática o afines"
    result5 = compare_education(cv_education, job_education)
    print(f"Puntaje: {result5['score']}")
    print(f"Coinciden: {len(result5['matched'])} educaciones")
    print(f"Faltan: {result5['missing']}")
    print(f"Razón: {result5['reason']}")
    
    # Mostrar detalles de las coincidencias
    if result5['matched']:
        print("\nDetalles de coincidencias:")
        for match in result5['matched']:
            print(f"  CV: {match['cv_education']} -> Requerido: {match['job_requirement']} (Score: {match['score']})")
    
def test_with_real_examples():
    """
    Prueba con ejemplos reales del proyecto - OPTIMIZADO: Una sola llamada a IA
    """
    print("\n=== TEST CON EJEMPLOS REALES (OPTIMIZADO) ===\n")
    
    # Ejemplo del CV real
    cv_education = [
        {
            "degree": "ingeniería de sistemas y computación",
            "institution": "universidad de los andes",
            "year": "2023",
            "field": "ingeniería de sistemas"
        },
        {
            "degree": "bachiller académico",
            "institution": "colegio bilingue lisa meitner",
            "year": "2018",
            "field": "educación secundaria"
        }
    ]
    
    # Ejemplo de la descripción de trabajo
    job_education = "egresado de la carreras técnicas o universitarias de ingeniería de sistemas computación ingeniería informática o afines"
    
    result = compare_education(cv_education, job_education)
    print(f"Puntaje total: {result['score']}")
    print(f"Educaciones coincidentes: {len(result['matched'])}")
    print(f"Requisitos faltantes: {len(result['missing'])}")
    print(f"Razón general: {result['reason']}")
    
    if result['matched']:
        print("\nEducaciones que coinciden:")
        for match in result['matched']:
            print(f"  ✓ {match['cv_education']} -> {match['job_requirement']} (Score: {match['score']})")
    
    if result['missing']:
        print("\nRequisitos faltantes:")
        for req in result['missing']:
            print(f"  ✗ {req}")

def test_education_variations():
    """
    Prueba específica para variaciones educativas y campos relacionados
    """
    print("\n=== TEST DE VARIACIONES EDUCATIVAS ===\n")
    
    # Diferentes tipos de educación técnica/universitaria
    education_variations = [
        {
            "degree": "ingeniería informática",
            "institution": "universidad nacional",
            "year": "2022",
            "field": "informática"
        },
        {
            "degree": "técnico en sistemas",
            "institution": "sena",
            "year": "2021",
            "field": "sistemas"
        },
        {
            "degree": "licenciatura en computación",
            "institution": "universidad distrital",
            "year": "2023",
            "field": "computación"
        },
        {
            "degree": "tecnología en desarrollo de software",
            "institution": "politécnico grancolombiano",
            "year": "2022",
            "field": "desarrollo de software"
        }
    ]
    
    job_education = "egresado de la carreras técnicas o universitarias de ingeniería de sistemas computación ingeniería informática o afines"
    
    for i, cv_education in enumerate(education_variations, 1):
        print(f"\n{i}. Probando: {cv_education['degree']}")
        result = compare_education([cv_education], job_education)
        print(f"   Puntaje: {result['score']}")
        print(f"   Razón: {result['reason']}")
        
        if result['matched']:
            for match in result['matched']:
                print(f"   ✓ {match['cv_education']} -> Score: {match['score']}")

if __name__ == "__main__":
    # Ejecutar escenarios simples
    test_education_comparator()
    
    # Ejecutar test con ejemplos reales
    test_with_real_examples()
    
    # Ejecutar test de variaciones
    test_education_variations()
