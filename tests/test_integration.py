import os
import pytest
from src.config import load_config
from src.llm_service import generate_script
from src.parser import parse_response
from src.prompt import build_prompt


@pytest.mark.integration
def test_fluxo_real_com_llm():
    if not os.getenv("LLM_API_KEY") and not os.path.exists(".env"):
        pytest.skip("Arquivo .env ausente para teste de integracao real.")

    config = load_config()
    prompt = build_prompt("Dica rapida sobre organizacao financeira para autonomos")
    raw = generate_script(prompt, config)
    parsed = parse_response(raw)

    assert len(parsed) > 20