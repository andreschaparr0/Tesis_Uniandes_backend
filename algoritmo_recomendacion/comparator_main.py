"""
Algoritmo principal que ejecuta todos los comparadores.
Compara un CV estructurado con una descripción de trabajo estructurada.
"""

import json
import sys
import os
from typing import Dict, Any

# Agregar el directorio padre al path para importar los comparadores
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from comparators.technical_skills_comparator import compare_technical_skills
from comparators.experience_comparator import compare_experience
from comparators.education_comparator import compare_education
from comparators.certifications_comparator import compare_certifications
from comparators.languages_comparator import compare_languages
from comparators.location_comparator import compare_locations
from comparators.responsibilities_comparator import compare_responsibilities
from comparators.soft_skills_comparator import compare_soft_skills


class ComparatorMain:
    """
    Clase principal que ejecuta todos los comparadores.
    """
    
    def load_json_file(self, file_path: str) -> Dict[str, Any]:
        """
        Carga un archivo JSON.
        
        Args:
            file_path (str): Ruta al archivo JSON
            
        Returns:
            dict: Contenido del JSON
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error cargando {file_path}: {e}")
            return {}
    
    def run_all_comparisons(self, cv_data: Dict[str, Any], job_data: Dict[str, Any]) -> Dict[str, Any]:
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
    
    def print_comparison_results(self, cv_data: Dict[str, Any], job_data: Dict[str, Any], results: Dict[str, Any]):
        """
        Imprime los resultados de todas las comparaciones.
        
        Args:
            cv_data (dict): Datos del CV
            job_data (dict): Datos del trabajo
            results (dict): Resultados de comparación
        """
        print("\n" + "="*50)
        print("RESULTADOS DE COMPARACIONES")
        print("="*50)
        
        # Información básica
        cv_name = cv_data.get('personal', {}).get('name', 'N/A')
        job_title = job_data.get('basic_info', {}).get('job_title', 'N/A')
        company = job_data.get('basic_info', {}).get('company_name', 'N/A')
        
        print(f"Candidato: {cv_name}")
        print(f"Posición: {job_title} en {company}")
        
        # Mostrar resultados de cada comparación
        for aspect, result in results.items():
            print(f"\n{aspect.replace('_', ' ').title()}:")
            print(f"  Score: {result.get('score', 0.0)}")
                        
            # Mostrar elementos faltantes
            missing = result.get('missing', [])
            if missing:
                print(f"  Faltantes: {missing}") 
            else:
                print(f"  Faltantes: No hay faltantes")
            # Mostrar razón si existe
            reason = result.get('reason', '')
            if reason:
                print(f"  Razón: {reason}")
            else:
                print(f"  Razón: No hay razón")
            # Mostrar coincidencias
            matched = result.get('matched', [])
            if matched:
                print(f"  Coincidencias: {matched}")
            else:
                print(f"  Coincidencias: No hay coincidencias")
    def run_comparisons(self, cv_file_path: str, job_file_path: str):
        """
        Ejecuta todas las comparaciones entre CV y descripción de trabajo.
        
        Args:
            cv_file_path (str): Ruta al archivo JSON del CV
            job_file_path (str): Ruta al archivo JSON de la descripción de trabajo
            
        Returns:
            tuple: (cv_data, job_data, results) o None si hay error
        """
        # Cargar datos
        cv_data = self.load_json_file(cv_file_path)
        job_data = self.load_json_file(job_file_path)
        if not cv_data or not job_data:
            print("Error: No se pudieron cargar los archivos JSON")
            return None
        # Ejecutar todas las comparaciones
        results = self.run_all_comparisons(cv_data, job_data)
        return cv_data, job_data, results


