import re
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import unicodedata

# Asegúrate de haber ejecutado previamente:
# import nltk; nltk.download('stopwords')

def quitar_simbolos_raros(text):
    """
    Quita símbolos raros como §, ï y otros caracteres especiales problemáticos.
    """
    # Lista de símbolos raros comunes
    simbolos_raros = "§ïîíìòóôõöøùúûüýÿñç"
    text = re.sub(f"[{re.escape(simbolos_raros)}]", "", text)
    return text

def quitar_tildes(text):
    """
    Convierte las letras con tilde a su versión sin tilde (ej: 'computación' -> 'computacion').
    """
    # Diccionario de conversión de caracteres con tilde a sin tilde
    conversiones = {
        'á': 'a', 'à': 'a', 'ä': 'a', 'â': 'a', 'ã': 'a', 'å': 'a',
        'é': 'e', 'è': 'e', 'ë': 'e', 'ê': 'e',
        'í': 'i', 'ì': 'i', 'ï': 'i', 'î': 'i',
        'ó': 'o', 'ò': 'o', 'ö': 'o', 'ô': 'o', 'õ': 'o', 'ø': 'o',
        'ú': 'u', 'ù': 'u', 'ü': 'u', 'û': 'u',
        'ý': 'y', 'ÿ': 'y',
        'ñ': 'n', 'ç': 'c',
        'Á': 'A', 'À': 'A', 'Ä': 'A', 'Â': 'A', 'Ã': 'A', 'Å': 'A',
        'É': 'E', 'È': 'E', 'Ë': 'E', 'Ê': 'E',
        'Í': 'I', 'Ì': 'I', 'Ï': 'I', 'Î': 'I',
        'Ó': 'O', 'Ò': 'O', 'Ö': 'O', 'Ô': 'O', 'Õ': 'O', 'Ø': 'O',
        'Ú': 'U', 'Ù': 'U', 'Ü': 'U', 'Û': 'U',
        'Ý': 'Y', 'Ÿ': 'Y',
        'Ñ': 'N', 'Ç': 'C'
    }
    
    # Aplicar las conversiones
    for caracter_con_tilde, caracter_sin_tilde in conversiones.items():
        text = text.replace(caracter_con_tilde, caracter_sin_tilde)
    
    return text

def unir_letras_separadas(text):
    """
    Une secuencias de letras separadas por espacios (ej: 'G I T H U B' -> 'GITHUB').
    También funciona con palabras tipo 'P r o b l e m - S o l v i n g'.
    """
    def repl(match):
        return match.group(0).replace(' ', '')
    # Unir letras separadas por espacios (mínimo 2 letras)
    return re.sub(r'(?<!\w)([A-Za-z](?:\s+[A-Za-z]){1,})(?!\w)', repl, text)

def clean_text(text):
    """
    Limpia y normaliza un texto eliminando caracteres especiales, puntuación, números,
    stopwords y aplicando stemming. Devuelve el texto limpio y en minúsculas.
    Además, une palabras que aparecen con letras separadas por espacios.
    """
    # PRIMERO: Convertir tildes y acentos (antes de eliminar símbolos)
    text = quitar_tildes(text)
    
    # SEGUNDO: Quitar símbolos raros (después de convertir tildes)
    text = quitar_simbolos_raros(text)
    
    # TERCERO: Unir letras separadas por espacios
    text = unir_letras_separadas(text)

    # Eliminar caracteres especiales personalizados
    special_characters = "○●•◦"
    text = re.sub(f"[{re.escape(special_characters)}]", "", text)

    # Eliminar puntuación
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Eliminar números
    #text = re.sub(r'\d+', '', text)

    # Eliminar espacios extra
    #text = " ".join(text.split())

    # Convertir a minúsculas
    text = text.lower()

    # Eliminar stopwords
    #stop_words = set(stopwords.words('english'))
    #text = " ".join(word for word in text.split() if word not in stop_words)

    # Stemming
    #ps = PorterStemmer()
    #text = " ".join(ps.stem(word) for word in text.split())

    return text

