"""
Módulo de limpieza de datos para el sistema de recomendación de CVs.
Se encarga de extraer texto de PDFs y limpiar descripciones de trabajo.
"""

import os
import fitz  # PyMuPDF
from typing import Tuple, Optional
import re
import sys

# Agregar el directorio src al path para importar las funciones del proyecto
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
from limpieza.limpieza import clean_text
from limpieza.pdf_text_extractor import extract_text_from_pdf


class DataCleaner:
    """
    Clase para limpiar y extraer datos de CVs (PDFs) y descripciones de trabajo.
    """
    
    def __init__(self):
        """
        Inicializa el limpiador de datos.
        """
        self.supported_formats = ['.pdf']
    
    def clean_cv_from_image(self, image_path: str) -> str:
        """
        Extrae y limpia el texto de un CV desde un archivo PDF.
        
        Args:
            image_path (str): Ruta al archivo PDF del CV
            
        Returns:
            str: Texto limpio extraído del CV
            
        Raises:
            FileNotFoundError: Si el archivo no existe
            ValueError: Si el formato no es soportado
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"El archivo {image_path} no existe")
        
        # Verificar formato
        file_extension = os.path.splitext(image_path)[1].lower()
        if file_extension not in self.supported_formats:
            raise ValueError(f"Formato {file_extension} no soportado. Formatos soportados: {self.supported_formats}")
        
        try:
            # Extraer texto usando la función específica del proyecto
            text_content = extract_text_from_pdf(image_path)
            
            # Limpiar el texto extraído usando la función específica del proyecto
            cleaned_text = clean_text(text_content)
            
            return cleaned_text
            
        except Exception as e:
            raise Exception(f"Error al procesar el archivo PDF {image_path}: {str(e)}")
    
    def clean_job_description(self, description_path: str) -> str:
        """
        Limpia y extrae el texto de una descripción de trabajo.
        
        Args:
            description_path (str): Ruta al archivo de descripción de trabajo
            
        Returns:
            str: Texto limpio de la descripción
            
        Raises:
            FileNotFoundError: Si el archivo no existe
        """
        if not os.path.exists(description_path):
            raise FileNotFoundError(f"El archivo {description_path} no existe")
        
        try:
            # Leer el archivo
            with open(description_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Limpiar el texto usando la función específica del proyecto
            cleaned_text = clean_text(content)
            
            return cleaned_text
            
        except Exception as e:
            raise Exception(f"Error al procesar la descripción {description_path}: {str(e)}")
    
    
    def process_both_files(self, cv_path: str, description_path: str) -> Tuple[str, str]:
        """
        Procesa tanto el CV como la descripción de trabajo en una sola operación.
        
        Args:
            cv_path (str): Ruta al archivo PDF del CV
            description_path (str): Ruta al archivo de descripción de trabajo
            
        Returns:
            Tuple[str, str]: Tupla con (texto_cv_limpio, texto_descripcion_limpia)
        """
        try:
            cv_text = self.clean_cv_from_image(cv_path)
            description_text = self.clean_job_description(description_path)
            
            return cv_text, description_text
            
        except Exception as e:
            raise Exception(f"Error al procesar los archivos: {str(e)}")

