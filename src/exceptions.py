class AppError(Exception):
    """Exceção base para erros controlados da aplicação."""


class InputValidationError(AppError):
    """Erro quando a entrada do usuário é vazia ou inválida."""


class ConfigurationError(AppError):
    """Erro quando variáveis de ambiente ou credenciais estão ausentes ou inválidas."""


class LLMCommunicationError(AppError):
    """Erro de rede, timeout, autenticação recusada ou indisponibilidade do provedor."""


class ResponseParsingError(AppError):
    """Erro quando o modelo retorna resposta vazia ou fora do formato esperado."""