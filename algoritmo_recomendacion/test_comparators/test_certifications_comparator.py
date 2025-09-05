"""
Test para el comparador de certificaciones
"""

import sys
import os
# Agregar el directorio padre al path para importar el comparador
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from comparators.certifications_comparator import compare_certifications, get_certification_score

def test_certifications_comparator():
    """
    Prueba el comparador de certificaciones con datos de ejemplo
    """
    print("=== TEST DEL COMPARADOR DE CERTIFICACIONES ===\n")
    
    # Datos de ejemplo
    cv_certifications = [
        "AWS Certified Solutions Architect",
        "Google Cloud Professional",
        "Microsoft Azure Fundamentals"
    ]
    
    job_certifications = [
        "AWS Certified Solutions Architect",
        "Cisco CCNA",
        "CompTIA Security+"
    ]
    
    print("Certificaciones del CV:", cv_certifications)
    print("Certificaciones requeridas:", job_certifications)
    print()
    
    # Realizar comparación
    result = compare_certifications(cv_certifications, job_certifications)
    
    # Mostrar resultados
    print("=== RESULTADOS DE LA COMPARACIÓN ===")
    print(f"Puntaje: {result['score']}")
    print(f"Certificaciones que coinciden: {result['matched']}")
    print(f"Certificaciones faltantes: {result['missing']}")
    print()
    
    # Calcular puntaje final
    score = get_certification_score(result)
    print(f"Puntaje final: {score:.2f}")
    
    return result

def test_simple_scenarios():
    """
    Prueba escenarios simples
    """
    print("\n=== TEST DE ESCENARIOS SIMPLES ===\n")
    
    # Escenario 1: CV con certificación exacta
    print("1. CV con certificación exacta:")
    cv_certs = ["AWS Certified Solutions Architect"]
    job_certs = ["AWS Certified Solutions Architect"]
    result1 = compare_certifications(cv_certs, job_certs)
    print(f"Puntaje: {result1['score']}")
    print(f"Coinciden: {result1['matched']}")
    print(f"Faltan: {result1['missing']}")
    
    # Escenario 2: CV sin certificaciones requeridas
    print("\n2. CV sin certificaciones requeridas:")
    cv_certs = ["Microsoft Office Specialist"]
    job_certs = ["AWS Certified Solutions Architect"]
    result2 = compare_certifications(cv_certs, job_certs)
    print(f"Puntaje: {result2['score']}")
    print(f"Coinciden: {result2['matched']}")
    print(f"Faltan: {result2['missing']}")
    
    # Escenario 3: Sin certificaciones requeridas
    print("\n3. Sin certificaciones requeridas:")
    result3 = compare_certifications(["AWS Certified"], [])
    print(f"Puntaje: {result3['score']}")
    print(f"Coinciden: {result3['matched']}")
    print(f"Faltan: {result3['missing']}")
    
    # Escenario 4: Múltiples certificaciones
    print("\n4. Múltiples certificaciones:")
    cv_certs = ["AWS Certified Solutions Architect", "Google Cloud Professional", "Microsoft Azure Fundamentals"]
    job_certs = ["AWS Certified Solutions Architect", "Cisco CCNA"]
    result4 = compare_certifications(cv_certs, job_certs)
    print(f"Puntaje: {result4['score']}")
    print(f"Coinciden: {result4['matched']}")
    print(f"Faltan: {result4['missing']}")
    
    # Escenario 5: Certificación similar pero no exacta
    print("\n5. Certificación similar pero no exacta:")
    cv_certs = ["AWS Solutions Architect Associate"]
    job_certs = ["AWS Certified Solutions Architect"]
    result5 = compare_certifications(cv_certs, job_certs)
    print(f"Puntaje: {result5['score']}")
    print(f"Coinciden: {result5['matched']}")
    print(f"Faltan: {result5['missing']}")

if __name__ == "__main__":
    # Ejecutar test principal
    test_certifications_comparator()
    
    # Ejecutar escenarios simples
    test_simple_scenarios()
    
    print("\n=== FIN DE LOS TESTS ===")
