from groq import Groq
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(dotenv_path=Path('../.env'))

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def query_groq(messages: list, model: str = "llama-3.3-70b-versatile", temperature: float = 0):
    """
    Function to query the GROQ API with a list of messages.
    
    Args:
        messages (list): The list of messages to send to the model.
        model (str): The model to use for the completion.
        temperature (float): The temperature to use for the completion.
        
    Returns:
        str: The completion from the model.
    """
    chat_completion = client.chat.completions.create(
        messages=messages,
        
        model=model,

        # Controls randomness: lowering results in less random completions.
        # As the temperature approaches zero, the model will become deterministic and repetitive.
        temperature=temperature,
    )

    return chat_completion.choices[0].message.content