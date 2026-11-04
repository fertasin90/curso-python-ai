
from pydantic import ValidationError
from config import LLMConfig


def probar_configuracion(nombre, temperature, max_tokens):

    print(f"\nPrueba: {nombre}")

    try:
        config = LLMConfig(
            provider="openai",
            model="gpt-4o-mini",
            prompt="Hola",
            temperature=temperature,
            max_tokens=max_tokens
        )

        print("VALIDO:", config)

    except ValidationError as error:
        print("ERROR DE VALIDACION:")
        print(error)


probar_configuracion("Parametros correctos", 0.7, 500)

probar_configuracion("Temperatura invalida", 5, 500)

probar_configuracion("Tokens negativos", 0.7, -10)
