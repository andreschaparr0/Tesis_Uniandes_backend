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
    
    def generate_recommendation(self, cv_data: dict, job_data: dict, weights: dict = None) -> dict:
        """
        Genera la recomendación usando ComparatorMain.
        
        Args:
            cv_data (dict): Datos del CV estructurado
            job_data (dict): Datos de la descripción de trabajo estructurada
            weights (dict): Pesos para el cálculo del score final
            
        Returns:
            dict: Resultados de las comparaciones con score final
        """
        try:
            # Usar ComparatorMain para ejecutar todas las comparaciones
            results = self.comparator.run_all_comparisons(cv_data, job_data)
            
            # Calcular score final
            final_score_data = self.comparator.calculate_final_score(results, weights)
            
            # Combinar resultados con score final
            recommendation = {
                'comparison_results': results,
                'final_score_data': final_score_data
            }
            
            return recommendation
            
        except Exception as e:
            print(f"Error al generar recomendación: {e}")
            return {}
    
    def print_recommendation_results(self, cv_data: dict, job_data: dict, recommendation: dict, weights: dict = None):
        """
        Imprime los resultados de la recomendación usando ComparatorMain.
        
        Args:
            cv_data (dict): Datos del CV estructurado
            job_data (dict): Datos de la descripción de trabajo estructurada
            recommendation (dict): Resultados completos de la recomendación
            weights (dict): Pesos para el cálculo del score final
        """
        try:
            # Extraer resultados de comparación
            if 'comparison_results' in recommendation:
                results = recommendation['comparison_results']
            else:
                results = recommendation
            
            # Usar el método print_comparison_results de ComparatorMain
            self.comparator.print_comparison_results(cv_data, job_data, results, weights)
            
        except Exception as e:
            print(f"Error al imprimir resultados: {e}")
    
    def get_final_score(self, recommendation: dict) -> float:
        """
        Obtiene el score final de una recomendación.
        
        Args:
            recommendation (dict): Resultados completos de la recomendación
            
        Returns:
            float: Score final (0.0 - 1.0)
        """
        try:
            if 'final_score_data' in recommendation:
                return recommendation['final_score_data']['final_score']
            else:
                return 0.0
        except Exception as e:
            print(f"Error al obtener score final: {e}")
            return 0.0
    
    def get_score_breakdown(self, recommendation: dict) -> dict:
        """
        Obtiene el desglose detallado del score.
        
        Args:
            recommendation (dict): Resultados completos de la recomendación
            
        Returns:
            dict: Desglose del score por aspecto
        """
        try:
            if 'final_score_data' in recommendation:
                return recommendation['final_score_data']['score_breakdown']
            else:
                return {}
        except Exception as e:
            print(f"Error al obtener desglose del score: {e}")
            return {}

