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
    
    # Escenario 4: Sin certificaciones requeridas (sin habilidades técnicas)
    print("\n4. Sin certificaciones requeridas (sin habilidades técnicas):")
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
    
    # Escenario 6: Sin certificaciones requeridas pero con habilidades técnicas (NUEVA FUNCIONALIDAD)
    print("\n6. Sin certificaciones requeridas pero comparando con habilidades técnicas:")
    cv_certs = [
        {
            "name": "aws certified solutions architect",
            "issuer": "amazon web services",
            "year": "2023"
        },
        {
            "name": "kubernetes administrator certification",
            "issuer": "linux foundation",
            "year": "2024"
        }
    ]
    job_certs = []
    job_tech_skills = ["aws", "kubernetes", "docker", "terraform", "python"]
    result6 = compare_certifications(cv_certs, job_certs, job_tech_skills)
    print(f"Puntaje: {result6['score']}")
    print(f"Razón: {result6['reason']}")
    
    # Escenario 7: Certificaciones no relacionadas con habilidades técnicas
    print("\n7. Certificaciones no relacionadas con habilidades técnicas:")
    cv_certs = [
        {
            "name": "diplomado en liderazgo",
            "issuer": "universidad",
            "year": "2023"
        }
    ]
    job_certs = []
    job_tech_skills = ["java", "spring boot", "microservices", "sql"]
    result7 = compare_certifications(cv_certs, job_certs, job_tech_skills)
    print(f"Puntaje: {result7['score']}")
    print(f"Razón: {result7['reason']}")
    
    # Escenario 8: Certificaciones requeridas pero el CV solo tiene skills técnicas (NUEVA FUNCIONALIDAD)
    print("\n8. Certificaciones AWS requeridas, CV tiene skills en AWS (sin certificación):")
    cv_certs = []
    job_certs = ["certificados aws", "certificados kubernetes"]
    cv_tech_skills = ["aws", "ec2", "s3", "lambda", "kubernetes", "docker"]
    result8 = compare_certifications(cv_certs, job_certs, None, cv_tech_skills)
    print(f"Puntaje: {result8['score']}")
    print(f"Razón: {result8['reason']}")
    
    # Escenario 9: Certificaciones requeridas, CV tiene certificaciones Y skills técnicas (mejor caso)
    print("\n9. Certificaciones requeridas, CV tiene certificación AWS Y skills relacionadas:")
    cv_certs = [
        {
            "name": "aws certified solutions architect",
            "issuer": "amazon web services",
            "year": "2023"
        }
    ]
    job_certs = ["certificados aws", "certificados google cloud"]
    cv_tech_skills = ["aws", "ec2", "s3", "lambda", "google cloud platform", "gcp"]
    result9 = compare_certifications(cv_certs, job_certs, None, cv_tech_skills)
    print(f"Puntaje: {result9['score']}")
    print(f"Razón: {result9['reason']}")
    
    # Escenario 10: Certificaciones requeridas, CV sin certificaciones ni skills relevantes
    print("\n10. Certificaciones AWS requeridas, CV sin certificaciones ni skills relacionadas:")
    cv_certs = []
    job_certs = ["certificados aws"]
    cv_tech_skills = ["php", "wordpress", "mysql"]
    result10 = compare_certifications(cv_certs, job_certs, None, cv_tech_skills)
    print(f"Puntaje: {result10['score']}")
    print(f"Razón: {result10['reason']}")
    
    #

if __name__ == "__main__":
    # Ejecutar escenarios de prueba
    test_certifications_comparator()
