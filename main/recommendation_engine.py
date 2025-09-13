"""
Módulo de recomendación que usa ComparatorMain para ejecutar comparaciones.
"""

import sys
import os

# Agregar el directorio algoritmo_recomendacion al path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'algoritmo_recomendacion'))

from comparator_main import ComparatorMain


class RecommendationEngine:
    """
    Motor de recomendación que usa ComparatorMain.
    """
    
    def __init__(self):
        """
        Inicializa el motor de recomendación.
        """
        self.comparator = ComparatorMain()
    
    def generate_recommendation(self, cv_data: dict, job_data: dict) -> dict:
        """
        Genera la recomendación usando ComparatorMain.
        
        Args:
            cv_data (dict): Datos del CV estructurado
            job_data (dict): Datos de la descripción de trabajo estructurada
            
        Returns:
            dict: Resultados de las comparaciones
        """
        try:
            # Usar ComparatorMain para ejecutar todas las comparaciones
            results = self.comparator.run_all_comparisons(cv_data, job_data)
            return results
            
        except Exception as e:
            print(f"Error al generar recomendación: {e}")
            return {}
    
    def print_recommendation_results(self, cv_data: dict, job_data: dict, results: dict):
        """
        Imprime los resultados de la recomendación usando ComparatorMain.
        
        Args:
            cv_data (dict): Datos del CV estructurado
            job_data (dict): Datos de la descripción de trabajo estructurada
            results (dict): Resultados de las comparaciones
        """
        try:
            # Usar el método print_comparison_results de ComparatorMain
            self.comparator.print_comparison_results(cv_data, job_data, results)
            
        except Exception as e:
            print(f"Error al imprimir resultados: {e}")

