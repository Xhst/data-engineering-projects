import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')


def clean_and_tokenize(text: str, language: str = 'english') -> list[str]:
    tokens = word_tokenize(text)
    
    stop_words = set(stopwords.words(language))
    
    cleaned_tokens = [
        word.lower() for word in tokens
        if word.isalpha() and  
           word.lower() not in stop_words and 
           word not in string.punctuation  
    ]
    
    return cleaned_tokens


def filter(text: str) -> str:
    result = (" ".join(clean_and_tokenize(text)))

    return result

