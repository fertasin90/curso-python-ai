
import os
from typing import AsyncGenerator

import openai
import anthropic

from dotenv import load_dotenv
from config import LLMConfig


# ==========================================
# VARIABLES DE ENTORNO
# ==========================================

load_dotenv()


# ==========================================
# ASYNC LLM MANAGER
# ==========================================

class AsyncLLMManager:

    def __init__(self, provider: str):

        self.provider = provider.lower()

        # OPENAI
        if self.provider == "openai":

            api_key = os.getenv("OPENAI_API_KEY")

            if not api_key:
                raise ValueError(
                    "Falta OPENAI_API_KEY en el archivo .env"
                )

            self.client = openai.AsyncOpenAI(
                api_key=api_key,
                max_retries=0,
                timeout=30.0
            )

        # ANTHROPIC
        elif self.provider == "anthropic":

            api_key = os.getenv("ANTHROPIC_API_KEY")

            if not api_key:
                raise ValueError(
                    "Falta ANTHROPIC_API_KEY en el archivo .env"
                )

            self.client = anthropic.AsyncAnthropic(
                api_key=api_key,
                max_retries=0,
                timeout=30.0
            )

        else:
            raise ValueError(
                "Proveedor no soportado. "
                "Utilizar 'openai' o 'anthropic'."
            )

    # ==========================================
    # GENERACION ASINCRONA CON STREAMING
    # ==========================================

    async def generate(
        self,
        config: LLMConfig
    ) -> AsyncGenerator[str, None]:

        if config.provider != self.provider:
            yield (
                "ERROR: El proveedor no coincide "
                "con la configuración."
            )
            return

        try:

            # ==================================
            # OPENAI
            # ==================================

            if self.provider == "openai":

                stream = await self.client.chat.completions.create(
                    model=config.model,
                    messages=[
                        {
                            "role": "user",
                            "content": config.prompt
                        }
                    ],
                    temperature=config.temperature,
                    max_tokens=config.max_tokens,
                    stream=True
                )

                async for chunk in stream:

                    if not chunk.choices:
                        continue

                    content = chunk.choices[0].delta.content

                    if content:
                        yield content

            # ==================================
            # ANTHROPIC
            # ==================================

            elif self.provider == "anthropic":

                stream = await self.client.messages.create(
                    model=config.model,
                    max_tokens=config.max_tokens,
                    messages=[
                        {
                            "role": "user",
                            "content": config.prompt
                        }
                    ],
                    stream=True
                )

                async for event in stream:

                    if event.type == "content_block_delta":

                        if event.delta.type == "text_delta":

                            if event.delta.text:
                                yield event.delta.text

        # ======================================
        # RATE LIMITING
        # ======================================

        except (
            openai.RateLimitError,
            anthropic.RateLimitError
        ) as error:

            error_code = ""

            if isinstance(error, openai.RateLimitError):

                body = error.body

                if isinstance(body, dict):

                    error_code = body.get("code", "")

                    if not error_code:

                        nested = body.get("error", {})

                        if isinstance(nested, dict):
                            error_code = nested.get("code", "")

            if error_code == "insufficient_quota":

                yield (
                    "\nERROR: Créditos o cuota insuficientes "
                    "en OpenAI API."
                )

            else:

                yield (
                    "\nERROR: Límite de solicitudes "
                    "alcanzado (Rate Limit)."
                )

        # ======================================
        # ERRORES DE CONEXION
        # ======================================

        except (
            openai.APIConnectionError,
            anthropic.APIConnectionError
        ):

            yield (
                "\nERROR: No se pudo establecer "
                "conexión con la API."
            )

        # ======================================
        # ERRORES GENERALES DE API
        # ======================================

        except (
            openai.APIError,
            anthropic.APIError
        ) as error:

            yield (
                "\nERROR: Falló la solicitud a la API "
                f"({type(error).__name__})."
            )

        # ======================================
        # ERRORES INESPERADOS
        # ======================================

        except Exception as error:

            yield (
                "\nERROR inesperado: "
                f"{type(error).__name__}: {error}"
            )
