"""
Módulo de comparaciones para el sistema de recomendación de CVs.
Ejecuta todos los comparadores y calcula el score final.
"""

import sys
import os

# Agregar el directorio algoritmo_recomendacion al path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'algoritmo_recomendacion'))

from comparators.technical_skills_comparator import compare_technical_skills
from comparators.experience_comparator import compare_experience
from comparators.education_comparator import compare_education
from comparators.certifications_comparator import compare_certifications
from comparators.languages_comparator import compare_languages
from comparators.location_comparator import compare_locations
from comparators.responsibilities_comparator import compare_responsibilities
from comparators.soft_skills_comparator import compare_soft_skills


class RecommendationEngine:
    """
    Motor de recomendación que ejecuta todas las comparaciones.
    """
    
    def __init__(self):
        """
        Inicializa el motor de recomendación.
        """
        self.weights = {
            'technical_skills': 0.25,
            'experience': 0.20,
            'education': 0.15,
            'certifications': 0.10,
            'languages': 0.10,
            'location': 0.05,
            'responsibilities': 0.10,
            'soft_skills': 0.05
        }
    
    def run_all_comparisons(self, cv_data: dict, job_data: dict) -> dict:
        """
        Ejecuta todas las comparaciones entre CV y descripción de trabajo.
        
        Args:
            cv_data (dict): Datos del CV estructurado
            job_data (dict): Datos de la descripción de trabajo estructurada
            
        Returns:
            dict: Resultados de todas las comparaciones
        """
        results = {}
        
        # 1. Habilidades técnicas
        cv_skills = cv_data.get('technical_skills', [])
        job_skills = job_data.get('technical_skills', [])
        results['technical_skills'] = compare_technical_skills(cv_skills, job_skills)
        
        # 2. Experiencia
        cv_experience = cv_data.get('experience', [])
        job_experience = job_data.get('experience', '')
        results['experience'] = compare_experience(cv_experience, job_experience)
        
        # 3. Educación
        cv_education = cv_data.get('education', [])
        job_education = job_data.get('education', '')
        results['education'] = compare_education(cv_education, job_education)
        
        # 4. Certificaciones
        cv_certifications = cv_data.get('certifications', [])
        job_certifications = job_data.get('certifications', [])
        results['certifications'] = compare_certifications(cv_certifications, job_certifications)
        
        # 5. Idiomas
        cv_languages = cv_data.get('languages', {})
        job_languages = job_data.get('languages', {})
        results['languages'] = compare_languages(cv_languages, job_languages)
        
        # 6. Ubicación
        cv_location = {'location': cv_data.get('personal', {}).get('location', '')}
        job_location = {'location': job_data.get('location', '')}
        results['location'] = compare_locations(cv_location, job_location)
        
        # 7. Responsabilidades
        job_responsibilities = job_data.get('responsibilities', [])
        results['responsibilities'] = compare_responsibilities(cv_experience, job_responsibilities)
        
        # 8. Habilidades blandas
        cv_soft_skills = cv_data.get('soft_skills', [])
        job_soft_skills = job_data.get('soft_skills', [])
        results['soft_skills'] = compare_soft_skills(cv_soft_skills, job_soft_skills)
        
        return results
    
    def calculate_final_score(self, results: dict) -> float:
        """
        Calcula el score final ponderado.
        
        Args:
            results (dict): Resultados de todas las comparaciones
            
        Returns:
            float: Score final entre 0 y 1
        """
        total_score = 0.0
        total_weight = 0.0
        
        for aspect, result in results.items():
            if aspect in self.weights:
                score = result.get('score', 0.0)
                weight = self.weights[aspect]
                total_score += score * weight
                total_weight += weight
        
        if total_weight == 0:
            return 0.0
        
        return total_score / total_weight
    
    def generate_recommendation(self, cv_data: dict, job_data: dict) -> dict:
        """
        Genera la recomendación completa.
        
        Args:
            cv_data (dict): Datos del CV estructurado
            job_data (dict): Datos de la descripción de trabajo estructurada
            
        Returns:
            dict: Recomendación completa con score final
        """
        try:
            # Ejecutar todas las comparaciones
            results = self.run_all_comparisons(cv_data, job_data)
            
            # Calcular score final
            final_score = self.calculate_final_score(results)
            
            # Información básica
            cv_name = cv_data.get('personal', {}).get('name', 'N/A')
            job_title = job_data.get('basic_info', {}).get('job_title', 'N/A')
            company = job_data.get('basic_info', {}).get('company_name', 'N/A')
            
            recommendation = {
                'candidate': cv_name,
                'position': job_title,
                'company': company,
                'final_score': final_score,
                'results': results,
                'weights': self.weights
            }
            
            return recommendation
            
        except Exception as e:
            print(f"Error al generar recomendación: {e}")
            return {}

