import asyncio
import os

from dotenv import load_dotenv
from pydantic import ValidationError

from config import LLMConfig
from llm_manager import AsyncLLMManager

load_dotenv()


async def main():

    provider = os.getenv("LLM_PROVIDER", "openai").lower()

    models = {
        "openai": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "anthropic": os.getenv(
            "ANTHROPIC_MODEL", "claude-3-5-haiku-latest"
        ),
    }

    try:
        if provider not in models:
            raise ValueError("LLM_PROVIDER debe ser openai o anthropic")

        config = LLMConfig(
            provider=provider,
            model=models[provider],
            temperature=0.7,
            max_tokens=500,
            prompt="Explicá qué es AI Engineering en tres oraciones.",
        )

        manager = AsyncLLMManager(provider=config.provider)

        print(f"\nProveedor: {config.provider}")
        print(f"Modelo: {config.model}")
        print("\nRespuesta:\n")

        async for fragment in manager.generate(config):
            print(fragment, end="", flush=True)

        print()

    except (ValidationError, ValueError) as error:
        print(f"Error de configuración: {error}")


if __name__ == "__main__":
    asyncio.run(main())