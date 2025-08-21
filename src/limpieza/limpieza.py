import re
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Asegúrate de haber ejecutado previamente:
# import nltk; nltk.download('stopwords')

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
    # Unir letras separadas por espacios
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

# Ejemplo de uso:
if __name__ == "__main__":
    ejemplo = """
    John Doe
    Software Engineer
    G I T H U B: johndoe
    P r o b l e m - S o l v i n g
    Experience: Developed web applications using Python and JavaScript. 2020-2023
    Education: BSc in Computer Science
    Skills: Python, JavaScript, Machine Learning, Data Analysis
    """
    print("Texto original:\n", ejemplo)
    print("\nTexto limpio:\n", clean_text(ejemplo))
