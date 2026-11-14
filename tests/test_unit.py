from types import SimpleNamespace
from unittest.mock import MagicMock, patch
import pytest
from google.genai import errors as genai_errors
from src.cli import capture_input
from src.config import AppConfig, load_config
from src.exceptions import (
    ConfigurationError,
    InputValidationError,
    LLMCommunicationError,
    ResponseParsingError,
)
from src.llm_service import generate_script
from src.parser import parse_response
from src.prompt import build_prompt


def test_capture_input_rejeita_entrada_vazia(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "    ")
    with pytest.raises(InputValidationError, match="nao pode estar vazio"):
        capture_input()


def test_load_config_falha_quando_credencial_ausente(monkeypatch):
    monkeypatch.setattr("src.config.load_dotenv", lambda: None)
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    with pytest.raises(ConfigurationError, match="Credencial ausente"):
        load_config()


def test_load_config_falha_com_parametro_invalido(monkeypatch):
    monkeypatch.setattr("src.config.load_dotenv", lambda: None)
    monkeypatch.setenv("LLM_API_KEY", "chave-teste-valida")
    monkeypatch.setenv("LLM_TEMPERATURE", "texto-invalido")
    with pytest.raises(ConfigurationError, match="devem ser numericos"):
        load_config()


def test_build_prompt_inclui_ideia_do_cliente():
    prompt = build_prompt("Promocao de corte masculino")
    assert "Promocao de corte masculino" in prompt


def test_parse_response_rejeita_resposta_vazia():
    with pytest.raises(ResponseParsingError, match="conteudo vazio"):
        parse_response("   ")


def test_parse_response_aceita_roteiro_valido():
    texto = "GANCHO: Pare agora.\nDESENVOLVIMENTO: Conteudo.\nCTA: Clique no link."
    assert parse_response(texto) == texto


@patch("src.llm_service.genai.Client")
def test_generate_script_credencial_invalida(mock_client_cls):
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = genai_errors.ClientError(
        code=401, response_json={"error": {"message": "API key not valid"}}
    )
    mock_client_cls.return_value = mock_client

    config = AppConfig("chave-invalida", "gemini-3.5-flash-lite", 0.7, 500, 15)
    with pytest.raises(LLMCommunicationError, match="Credencial invalida"):
        generate_script("Teste", config)


@patch("src.llm_service.genai.Client")
def test_generate_script_indisponibilidade_servidor(mock_client_cls):
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = genai_errors.ServerError(
        code=503, response_json={"error": {"message": "Service unavailable"}}
    )
    mock_client_cls.return_value = mock_client

    config = AppConfig("chave-teste", "gemini-3.5-flash-lite", 0.7, 500, 15)
    with pytest.raises(LLMCommunicationError, match="temporariamente indisponivel"):
        generate_script("Teste", config)


@patch("src.llm_service.genai.Client")
def test_generate_script_timeout(mock_client_cls):
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = TimeoutError("Timed out")
    mock_client_cls.return_value = mock_client

    config = AppConfig("chave-teste", "gemini-3.5-flash-lite", 0.7, 500, 10)
    with pytest.raises(LLMCommunicationError, match="Tempo limite esgotado"):
        generate_script("Teste", config)


@patch("src.llm_service.genai.Client")
def test_generate_script_sucesso_simulado(mock_client_cls):
    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = SimpleNamespace(
        text="GANCHO: Olha isso.\nDESENVOLVIMENTO: Explicacao.\nCTA: Saiba mais."
    )
    mock_client_cls.return_value = mock_client

    config = AppConfig("chave-teste", "gemini-3.5-flash-lite", 0.7, 500, 15)
    resultado = generate_script("Teste", config)
    assert "GANCHO:" in resultado