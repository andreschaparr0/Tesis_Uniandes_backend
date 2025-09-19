"""
Test para el comparador de experiencia
"""

import sys
import os
# Agregar el directorio padre al path para importar el comparador
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from comparators.experience_comparator import compare_experience

def test_experience_comparator():
    """
    Prueba escenarios simples de comparación de experiencia
    """
    print("\n=== TEST DE ESCENARIOS DE EXPERIENCIA ===\n")
    
    # Escenario 1: Experiencia que cumple completamente
    print("1. Experiencia que cumple completamente:")
    cv_exp = [
        {
            "position": "desarrollador de software",
            "company": "empresa tech",
            "duration": "2020 – 2024",
            "description": "Desarrollé aplicaciones web con nodejs, trabajé en seguridad de la información, implementé sistemas de autenticación y manejo de datos sensibles."
        }
    ]
    job_exp = "contar con mínimo 4 años trabajando en posiciones similares, experiencia en seguridad de la información"
    result1 = compare_experience(cv_exp, job_exp)
    print(f"Puntaje: {result1['score']}")
    print(f"Razón: {result1['reason']}")
    
    # Escenario 2: Experiencia parcialmente relevante
    print("\n2. Experiencia parcialmente relevante:")
    cv_exp = [
        {
            "position": "desarrollador junior",
            "company": "startup",
            "duration": "2023 – 2024",
            "description": "Desarrollé aplicaciones web básicas con javascript y trabajé en proyectos pequeños."
        }
    ]
    job_exp = "contar con mínimo 4 años trabajando en posiciones similares, experiencia en seguridad de la información"
    result2 = compare_experience(cv_exp, job_exp)
    print(f"Puntaje: {result2['score']}")
    print(f"Razón: {result2['reason']}")
    
    # Escenario 3: Múltiples experiencias
    print("\n3. Múltiples experiencias:")
    cv_exp = [
        {
            "position": "desarrollador de software coop",
            "company": "caseware",
            "duration": "junio 2024 – junio 2025",
            "description": "Desarrollé apis restful con nodejs express y typescript, integrando autenticación jwt, diseñé y optimicé consultas en postgresql y mongodb."
        },
        {
            "position": "desarrollador de software",
            "company": "proyectos de portafolio",
            "duration": "abril 2024 – junio 2024",
            "description": "Desarrollé una api restful con nodejs express y typescript para gestionar datos de pacientes."
        }
    ]
    job_exp = "contar con mínimo 2 años trabajando en desarrollo de software, experiencia en nodejs y bases de datos"
    result3 = compare_experience(cv_exp, job_exp)
    print(f"Puntaje: {result3['score']}")
    print(f"Razón: {result3['reason']}")
    
    # Escenario 4: Sin experiencia requerida
    print("\n4. Sin experiencia requerida:")
    cv_exp = [
        {
            "position": "desarrollador de software",
            "company": "empresa",
            "duration": "2020 – 2024",
            "description": "Desarrollé aplicaciones web con nodejs."
        }
    ]
    job_exp = ""
    result4 = compare_experience(cv_exp, job_exp)
    print(f"Puntaje: {result4['score']}")
    print(f"Razón: {result4['reason']}")
    
    # Escenario 5: CV sin experiencia
    print("\n5. CV sin experiencia:")
    cv_exp = []
    job_exp = "contar con mínimo 3 años trabajando en desarrollo de software"
    result5 = compare_experience(cv_exp, job_exp)
    print(f"Puntaje: {result5['score']}")
    print(f"Razón: {result5['reason']}")
    
    # Escenario 6: Experiencia no relacionada
    print("\n6. Experiencia no relacionada:")
    cv_exp = [
        {
            "position": "contador",
            "company": "empresa contable",
            "duration": "2020 – 2024",
            "description": "Manejé libros contables y preparé estados financieros."
        }
    ]
    job_exp = "contar con mínimo 3 años trabajando en desarrollo de software"
    result6 = compare_experience(cv_exp, job_exp)
    print(f"Puntaje: {result6['score']}")
    print(f"Razón: {result6['reason']}")

if __name__ == "__main__":
    # Ejecutar escenarios de prueba
    test_experience_comparator()
