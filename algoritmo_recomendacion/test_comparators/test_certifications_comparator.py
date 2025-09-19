"""
Test para el comparador de certificaciones
"""

import sys
import os
# Agregar el directorio padre al path para importar el comparador
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from comparators.certifications_comparator import compare_certifications

def test_certifications_comparator():
    """
    Prueba escenarios simples de comparación de certificaciones
    """
    print("\n=== TEST DE ESCENARIOS DE CERTIFICACIONES ===\n")
    
    # Escenario 1: Certificación exacta
    print("1. Certificación exacta:")
    cv_certs = [
        {
            "name": "aws certified solutions architect",
            "issuer": "amazon web services",
            "year": "2023"
        }
    ]
    job_certs = ["certificados aws"]
    result1 = compare_certifications(cv_certs, job_certs)
    print(f"Puntaje: {result1['score']}")
    print(f"Razón: {result1['reason']}")
    
    # Escenario 2: Certificación relacionada
    print("\n2. Certificación relacionada:")
    cv_certs = [
        {
            "name": "certificado nvidia efficient large language model llm customization",
            "issuer": "nvidia",
            "year": "2025"
        }
    ]
    job_certs = ["certificados aws"]
    result2 = compare_certifications(cv_certs, job_certs)
    print(f"Puntaje: {result2['score']}")
    print(f"Razón: {result2['reason']}")
    
    # Escenario 3: Múltiples certificaciones
    print("\n3. Múltiples certificaciones:")
    cv_certs = [
        {
            "name": "aws certified solutions architect",
            "issuer": "amazon web services",
            "year": "2023"
        },
        {
            "name": "google cloud professional architect",
            "issuer": "google",
            "year": "2024"
        },
        {
            "name": "diplomado en liderazgo builders transform",
            "issuer": "colegio de estudios superiores de administración",
            "year": "2019"
        }
    ]
    job_certs = ["certificados aws", "certificados google cloud"]
    result3 = compare_certifications(cv_certs, job_certs)
    print(f"Puntaje: {result3['score']}")
    print(f"Razón: {result3['reason']}")
    
    # Escenario 4: Sin certificaciones requeridas
    print("\n4. Sin certificaciones requeridas:")
    cv_certs = [
        {
            "name": "aws certified solutions architect",
            "issuer": "amazon web services",
            "year": "2023"
        }
    ]
    job_certs = []
    result4 = compare_certifications(cv_certs, job_certs)
    print(f"Puntaje: {result4['score']}")
    print(f"Razón: {result4['reason']}")
    
    # Escenario 5: CV sin certificaciones
    print("\n5. CV sin certificaciones:")
    cv_certs = []
    job_certs = ["certificados aws", "certificados google cloud"]
    result5 = compare_certifications(cv_certs, job_certs)
    print(f"Puntaje: {result5['score']}")
    print(f"Razón: {result5['reason']}")
    
    #

if __name__ == "__main__":
    # Ejecutar escenarios de prueba
    test_certifications_comparator()
