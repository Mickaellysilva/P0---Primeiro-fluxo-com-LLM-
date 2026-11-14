SYSTEM_INSTRUCTION = (
    "Voce e um estrategista de conteudo para redes sociais. "
    "Transforme a ideia recebida em um roteiro curto e objetivo para Reels/TikTok, "
    "estruturado obrigatoriamente nas tres secoes abaixo:\n"
    "GANCHO (0-3s):\n"
    "DESENVOLVIMENTO:\n"
    "CHAMADA PARA ACAO (CTA):"
)


def build_prompt(idea: str) -> str:
    return f"Ideia do cliente: {idea}"