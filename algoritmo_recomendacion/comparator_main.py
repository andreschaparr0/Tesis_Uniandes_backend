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
        # print("Habilidades técnicas")
        # print(cv_skills)
        # print(job_skills)
        results['technical_skills'] = compare_technical_skills(cv_skills, job_skills)
            
        # 2. Experiencia
        cv_experience = cv_data.get('experience', [])
        job_experience = job_data.get('experience', '')
        # print("Experiencia")
        # print(cv_experience)
        # print(job_experience)
        results['experience'] = compare_experience(cv_experience, job_experience)
        
        # 3. Educación
        cv_education = cv_data.get('education', [])
        job_education = job_data.get('education', '')
        # print("Educación")
        # print(cv_education)
        # print(job_education)
        results['education'] = compare_education(cv_education, job_education)
        
        # 4. Certificaciones
        cv_certifications = cv_data.get('certifications', [])
        job_certifications = job_data.get('certifications', [])
        # print("Certificaciones")
        # print(cv_certifications)
        # print(job_certifications)
        # Pasar también las habilidades técnicas del job y del CV
        results['certifications'] = compare_certifications(cv_certifications, job_certifications, job_skills, cv_skills)
        
        # 5. Idiomas
        cv_languages = cv_data.get('languages', {})
        job_languages = job_data.get('languages', {})   
        # print("Idiomas")
        # print(cv_languages)
        # print(job_languages)
        results['languages'] = compare_languages(cv_languages, job_languages)
        
        # 6. Ubicación
        cv_location = {'location': cv_data.get('personal', {}).get('location', '')}
        job_location = {'location': job_data.get('location', '')}
        # print("Ubicación")
        # print(cv_location)
        # print(job_location)
        results['location'] = compare_locations(cv_location, job_location)
        
        # 7. Responsabilidades
        job_responsibilities = job_data.get('responsibilities', [])
        # print("Responsabilidades")
        # print(cv_experience)
        # print(job_responsibilities)
        results['responsibilities'] = compare_responsibilities(cv_experience, job_responsibilities)
        
        # 8. Habilidades blandas
        cv_soft_skills = cv_data.get('soft_skills', [])
        job_soft_skills = job_data.get('soft_skills', [])
        # print("Habilidades blandas")
        # print(cv_soft_skills)
        # print(job_soft_skills)
        results['soft_skills'] = compare_soft_skills(cv_soft_skills, job_soft_skills)
        
        return results
    
    def calculate_final_score(self, results: Dict[str, Any], weights: Dict[str, float] = None) -> Dict[str, Any]:
        """
        Calcula el score final ponderado basado en los resultados de las comparaciones.
        
        Args:
            results (dict): Resultados de todas las comparaciones
            weights (dict): Pesos para cada aspecto. Si es None, usa pesos predeterminados.
            
        Returns:
            dict: Score final y detalles del cálculo
        """
        # Pesos predeterminados
        default_weights = {
            'experience': 0.30,          # 30% - Muy importante  
            'technical_skills': 0.15,    # 15% - Muy importante
            'education': 0.15,           # 15% - Importante
            'responsibilities': 0.15,    # 15% - Importante
            'certifications': 0.10,      # 10% - Moderado
            'soft_skills': 0.08,         # 8% - Moderado
            'languages': 0.04,           # 4% - Bajo
            'location': 0.03             # 3% - Muy bajo
        }
        
        # Usar pesos proporcionados o los predeterminados
        if weights is None:
            weights = default_weights
        
        # Validar que los pesos sumen 1.0
        total_weight = sum(weights.values())
        if abs(total_weight - 1.0) > 0.01:  # Tolerancia de 0.01
            print(f"Advertencia: Los pesos suman {total_weight:.3f}, no 1.0. Normalizando...")
            weights = {k: v/total_weight for k, v in weights.items()}
        
        # Calcular score ponderado
        weighted_score = 0.0
        score_details = {}
        total_used_weight = 0.0
        
        for aspect, result in results.items():
            if aspect in weights:
                score = result.get('score', 0.0)
                weight = weights[aspect]
                
                # Si el score es -1, no se incluye en el cálculo
                if score == -1.0:
                    score_details[aspect] = {
                        'score': score,
                        'weight': weight,
                        'contribution': 0.0,
                        'ignored': True
                    }
                else:
                    contribution = score * weight
                    weighted_score += contribution
                    total_used_weight += weight
                    
                    score_details[aspect] = {
                        'score': score,
                        'weight': weight,
                        'contribution': contribution,
                        'ignored': False
                    }
        
        # Normalizar el score si se ignoraron algunos aspectos
        if total_used_weight > 0:
            normalized_score = weighted_score / total_used_weight
        else:
            normalized_score = 0.0
        
        return {
            'final_score': round(normalized_score, 3),
            'raw_score': round(weighted_score, 3),
            'weights_used': weights,
            'score_breakdown': score_details,
            'total_weight': sum(weights.values()),
            'used_weight': round(total_used_weight, 3),
            'ignored_aspects': [aspect for aspect, details in score_details.items() if details.get('ignored', False)]
        }
    
    def print_comparison_results(self, cv_data: Dict[str, Any], job_data: Dict[str, Any], results: Dict[str, Any], weights: Dict[str, float] = None):
        """
        Imprime los resultados de todas las comparaciones.
        
        Args:
            cv_data (dict): Datos del CV
            job_data (dict): Datos del trabajo
            results (dict): Resultados de comparación
            weights (dict): Pesos para el cálculo del score final
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
        
        # Calcular y mostrar score final
        final_score_data = self.calculate_final_score(results, weights)
        final_score = final_score_data['final_score']
        ignored_aspects = final_score_data.get('ignored_aspects', [])
        
        print(f"\n" + "-"*30)
        print(f"SCORE FINAL: {final_score:.1%}")
        if ignored_aspects:
            print(f"ASPECTOS IGNORADOS: {', '.join(ignored_aspects)}")
        print("-"*30)
        
        # Mostrar resultados de cada comparación
        for aspect, result in results.items():
            print(f"\n{aspect.replace('_', ' ').title()}:")
            score = result.get('score', 0.0)
            print(f"  Score: {score:.2f}")
            
            # Mostrar contribución al score final si está disponible
            if aspect in final_score_data['score_breakdown']:
                breakdown = final_score_data['score_breakdown'][aspect]
                weight = breakdown['weight']
                contribution = breakdown['contribution']
                ignored = breakdown.get('ignored', False)
                
                if ignored:
                    print(f"  Peso: {weight:.1%} | IGNORADO (sin datos)")
                else:
                    print(f"  Peso: {weight:.1%} | Contribución: {contribution:.3f}")
                        
            reason = result.get('reason', '')
            if reason:
                print(f"  Razón: {reason}")
            else:
                print(f"  Razón: No hay razón")

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


