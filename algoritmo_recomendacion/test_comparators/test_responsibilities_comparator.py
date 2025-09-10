"""
Test para el comparador de responsabilidades
"""

import sys
import os
# Agregar el directorio padre al path para importar el comparador
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from comparators.responsibilities_comparator import compare_responsibilities

def test_responsibilities_comparator():
    """
    Prueba escenarios simples de comparación de responsabilidades
    """
    print("\n=== TEST DE ESCENARIOS DE RESPONSABILIDADES ===\n")
    
    # Escenario 1: Experiencia que cumple con las responsabilidades
    print("1. Experiencia que cumple con las responsabilidades:")
    cv_exp = [
        {
            "position": "analista de seguridad de la información",
            "company": "empresa tech",
            "duration": "2020 – 2024",
            "description": "Supervisé la implementación de controles de seguridad, monitoreé riesgos de TI, establecí marcos de trabajo para evaluación de riesgos y administré cuentas de usuarios en sistemas empresariales."
        }
    ]
    job_resp = [
        "supervisar las actividades de planificación diseño e implementación de controles internos de ti y de seguridad para cumplir con las normativas vigentes",
        "monitorear y reportar la implementación de las acciones para mitigar los riesgos en las unidades de tecnologías de información"
    ]
    result1 = compare_responsibilities(cv_exp, job_resp)
    print(f"Puntaje: {result1['score']}")
    print(f"Coinciden: {len(result1['matched'])}")
    print(f"Faltan: {result1['missing']}")
    
    # Escenario 2: Experiencia parcialmente relevante
    print("\n2. Experiencia parcialmente relevante:")
    cv_exp = [
        {
            "position": "desarrollador de software",
            "company": "startup",
            "duration": "2022 – 2024",
            "description": "Desarrollé aplicaciones web con nodejs, implementé autenticación y autorización de usuarios, trabajé con bases de datos y configuré pipelines de despliegue."
        }
    ]
    job_resp = [
        "supervisar las actividades de planificación diseño e implementación de controles internos de ti y de seguridad para cumplir con las normativas vigentes",
        "establecer y monitorear la implementación de procedimientos de administración de cuentas de usuarios"
    ]
    result2 = compare_responsibilities(cv_exp, job_resp)
    print(f"Puntaje: {result2['score']}")
    print(f"Coinciden: {len(result2['matched'])}")
    print(f"Faltan: {result2['missing']}")
    
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
            "position": "analista de sistemas",
            "company": "empresa anterior",
            "duration": "2021 – 2023",
            "description": "Administré roles y permisos en sistemas SAP, monitoreé la implementación de controles de seguridad y reporté incidentes de seguridad."
        }
    ]
    job_resp = [
        "gestionar crear modificar eliminar los roles en sap",
        "establecer y mantener un marco de trabajo para evaluar y administrar los riesgos de tecnologías de información"
    ]
    result3 = compare_responsibilities(cv_exp, job_resp)
    print(f"Puntaje: {result3['score']}")
    print(f"Coinciden: {len(result3['matched'])}")
    print(f"Faltan: {result3['missing']}")
    
    # Escenario 4: Sin responsabilidades requeridas
    print("\n4. Sin responsabilidades requeridas:")
    cv_exp = [
        {
            "position": "desarrollador de software",
            "company": "empresa",
            "duration": "2020 – 2024",
            "description": "Desarrollé aplicaciones web con nodejs."
        }
    ]
    job_resp = []
    result4 = compare_responsibilities(cv_exp, job_resp)
    print(f"Puntaje: {result4['score']}")
    print(f"Coinciden: {len(result4['matched'])}")
    print(f"Faltan: {result4['missing']}")
    
    # Escenario 5: CV sin experiencia
    print("\n5. CV sin experiencia:")
    cv_exp = []
    job_resp = [
        "supervisar las actividades de planificación diseño e implementación de controles internos de ti y de seguridad"
    ]
    result5 = compare_responsibilities(cv_exp, job_resp)
    print(f"Puntaje: {result5['score']}")
    print(f"Coinciden: {len(result5['matched'])}")
    print(f"Faltan: {result5['missing']}")
    
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
    job_resp = [
        "supervisar las actividades de planificación diseño e implementación de controles internos de ti y de seguridad"
    ]
    result6 = compare_responsibilities(cv_exp, job_resp)
    print(f"Puntaje: {result6['score']}")
    print(f"Coinciden: {len(result6['matched'])}")
    print(f"Faltan: {result6['missing']}")

if __name__ == "__main__":
    # Ejecutar escenarios de prueba
    test_responsibilities_comparator()
