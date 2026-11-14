import os
from dataclasses import dataclass
from dotenv import load_dotenv
from src.exceptions import ConfigurationError


@dataclass(frozen=True)
class AppConfig:
    api_key: str
    model: str
    temperature: float
    max_tokens: int
    timeout: int


def load_config() -> AppConfig:
    load_dotenv()

    api_key = os.getenv("LLM_API_KEY", "").strip()
    if not api_key or api_key == "coloque_sua_chave_aqui":
        raise ConfigurationError(
            "Credencial ausente: configure a variavel LLM_API_KEY no arquivo .env."
        )

    model = os.getenv("LLM_MODEL", "gemini-3.5-flash-lite").strip()
    if not model:
        raise ConfigurationError(
            "Configuracao invalida: a variavel LLM_MODEL nao pode estar vazia."
        )

    try:
        temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        max_tokens = int(os.getenv("LLM_MAX_TOKENS", "500"))
        timeout = int(os.getenv("LLM_TIMEOUT", "15"))
    except ValueError as exc:
        raise ConfigurationError(
            "Configuracao invalida: LLM_TEMPERATURE, LLM_MAX_TOKENS e LLM_TIMEOUT devem ser numericos."
        ) from exc

    if not (0.0 <= temperature <= 2.0) or max_tokens <= 0 or timeout <= 0:
        raise ConfigurationError(
            "Configuracao invalida: verifique os limites de temperatura (0 a 2), tokens (>0) e timeout (>0)."
        )

    return AppConfig(
        api_key=api_key,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=timeout,
    )