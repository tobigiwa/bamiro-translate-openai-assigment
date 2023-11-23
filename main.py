from openai import OpenAI
from enum import Enum
import os, sys
from typing import NoReturn, TypeVar
from dotenv import load_dotenv


T = TypeVar("T")

class Language(Enum):
    "Language are the allowable target and existing languages."

    ENGLISH = "ENGLISH"
    FRENCH = "FRENCH"
    SPANISH = "SPANISH"
    CHINESE = "CHINESE"


def get_api_key() -> str:
    """returns openAI api key with key name `OPENAI_API_KEY` 
        from system enviroment variables.
    """

    key:str = "OPENAI_API_KEY"
    load_dotenv(verbose=True)

    apiKey = os.getenv(key)
    if apiKey is None:
        print(f"{key} not found", file=sys.stderr)
        sys.exit(1)
    
    return apiKey


client : OpenAI = OpenAI(
    api_key = get_api_key(),
    )

def translate(prompt:str,  target_lang: Language, exist_lang: Language,  column: T = None) -> T:
    """translate access `openAI gpt-3.5-turbo` model for `chat.completions`.

    bamiro, the generic type `T` is to account for the unknown `column`
    data structure in the question.
    """
    context = f"Translate the following text from {exist_lang.value} to {target_lang.value}:\n{prompt}"
    print(context)


    response = client.chat.completions.create( 
    model="gpt-3.5-turbo", 
    stream=True,
    messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": context}
        ],
     ) 

    print(response['choices'][0]['message']['content'])


def main() -> NoReturn:
    translate(prompt="how are you",exist_lang=Language.ENGLISH, target_lang=Language.FRENCH)

if __name__ == "__main__":
    main()

        



