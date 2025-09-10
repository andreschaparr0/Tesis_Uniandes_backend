"""
Test para el comparador de ubicaciones
"""

import sys
import os
# Agregar el directorio padre al path para importar el comparador
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from comparators.location_comparator import compare_locations

def test_location_comparator():
    """
    Prueba escenarios simples de comparación de ubicaciones
    """
    print("\n=== TEST DE ESCENARIOS DE UBICACIÓN ===\n")
    
    # Escenario 1: Ubicaciones idénticas
    print("1. Ubicaciones idénticas:")
    cv_loc = {"location": "bogota colombia"}
    job_loc = {"location": "bogota colombia"}
    result1 = compare_locations(cv_loc, job_loc)
    print(f"Puntaje: {result1['score']}")
    print(f"Coincide: {result1['matched']}")
    print(f"Razón: {result1['reason']}")
    
    # Escenario 2: Misma ciudad, diferente formato
    print("\n2. Misma ciudad, diferente formato:")
    cv_loc = {"location": "Bogotá, Colombia"}
    job_loc = {"location": "bogota colombia"}
    result2 = compare_locations(cv_loc, job_loc)
    print(f"Puntaje: {result2['score']}")
    print(f"Coincide: {result2['matched']}")
    print(f"Razón: {result2['reason']}")
    
    # Escenario 3: Mismo país, diferente ciudad
    print("\n3. Mismo país, diferente ciudad:")
    cv_loc = {"location": "medellin colombia"}
    job_loc = {"location": "bogota colombia"}
    result3 = compare_locations(cv_loc, job_loc)
    print(f"Puntaje: {result3['score']}")
    print(f"Coincide: {result3['matched']}")
    print(f"Razón: {result3['reason']}")
    
    # Escenario 4: Diferentes países
    print("\n4. Diferentes países:")
    cv_loc = {"location": "madrid españa"}
    job_loc = {"location": "bogota colombia"}
    result4 = compare_locations(cv_loc, job_loc)
    print(f"Puntaje: {result4['score']}")
    print(f"Coincide: {result4['matched']}")
    print(f"Razón: {result4['reason']}")
    
    # Escenario 5: Sin ubicación requerida
    print("\n5. Sin ubicación requerida:")
    cv_loc = {"location": "bogota colombia"}
    job_loc = {}
    result5 = compare_locations(cv_loc, job_loc)
    print(f"Puntaje: {result5['score']}")
    print(f"Coincide: {result5['matched']}")
    print(f"Razón: {result5['reason']}")
    
    # Escenario 6: CV sin ubicación
    print("\n6. CV sin ubicación:")
    cv_loc = {}
    job_loc = {"location": "bogota colombia"}
    result6 = compare_locations(cv_loc, job_loc)
    print(f"Puntaje: {result6['score']}")
    print(f"Coincide: {result6['matched']}")
    print(f"Razón: {result6['reason']}")
    

if __name__ == "__main__":
    # Ejecutar escenarios de prueba
    test_location_comparator()
