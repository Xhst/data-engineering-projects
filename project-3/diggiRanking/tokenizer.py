import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from typing import List


nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')


def tokenize(text: str, language: str = 'english') -> List[str]:
    
    # Tokenizza il testo
    tokens = word_tokenize(text)
    
    # Ottieni stop-words per la lingua specificata
    stop_words = set(stopwords.words(language))
    
    # Rimuovi punteggiatura, numeri e stop-words
    cleaned_tokens = [
        word.lower() for word in tokens
        if word.isalpha() and  # Filtra solo parole alfabetiche
           word.lower() not in stop_words and  # Rimuovi stop-words
           word not in string.punctuation  # Rimuovi punteggiatura
    ]
    
    return cleaned_tokens


def tokenize_toString(text: str) -> str:
    
    result = (" ".join(tokenize(text)))

    return result

