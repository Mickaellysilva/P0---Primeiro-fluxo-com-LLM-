from google import genai
from google.genai import errors as genai_errors
from google.genai import types
from src.config import AppConfig
from src.exceptions import LLMCommunicationError
from src.prompt import SYSTEM_INSTRUCTION


def generate_script(prompt: str, config: AppConfig) -> str:
    try:
        client = genai.Client(
            api_key=config.api_key,
            http_options={"timeout": config.timeout * 1000},
        )
        response = client.models.generate_content(
            model=config.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=config.temperature,
                max_output_tokens=config.max_tokens,
            ),
        )
        return response.text or ""
    except genai_errors.ClientError as exc:
        if exc.code in (401, 403):
            raise LLMCommunicationError(
                "Credencial invalida ou sem permissao: verifique sua chave LLM_API_KEY."
            ) from exc
        if exc.code == 404:
            raise LLMCommunicationError(
                f"Modelo '{config.model}' nao encontrado ou indisponivel para esta conta."
            ) from exc
        if exc.code == 429:
            raise LLMCommunicationError(
                "Limite de requisicoes atingido no provedor. Aguarde alguns instantes e tente novamente."
            ) from exc
        raise LLMCommunicationError(
            f"Falha na solicitacao ao provedor (codigo {exc.code}). Verifique os parametros enviados."
        ) from exc
    except genai_errors.ServerError as exc:
        raise LLMCommunicationError(
            "Servico temporariamente indisponivel no provedor do LLM (erro interno ou alta demanda)."
        ) from exc
    except TimeoutError as exc:
        raise LLMCommunicationError(
            f"Tempo limite esgotado ({config.timeout}s) aguardando resposta do LLM."
        ) from exc
    except Exception as exc:
        raise LLMCommunicationError(
            "Falha de comunicacao com o servico de LLM. Verifique sua conexao com a internet."
        ) from exc