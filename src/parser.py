from src.exceptions import ResponseParsingError


def parse_response(raw_text: str) -> str:
    if not isinstance(raw_text, str) or not raw_text.strip():
        raise ResponseParsingError(
            "Resposta invalida: o modelo retornou um conteudo vazio."
        )

    cleaned = raw_text.strip()
    if len(cleaned) < 15:
        raise ResponseParsingError(
            "Resposta inesperada: o retorno do modelo e curto demais para formar um roteiro."
        )

    return cleaned