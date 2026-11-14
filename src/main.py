import sys
from src.cli import capture_input, display_error, display_result
from src.config import load_config
from src.exceptions import AppError
from src.llm_service import generate_script
from src.parser import parse_response
from src.prompt import build_prompt


def run() -> int:
    try:
        config = load_config()
        idea = capture_input()
        prompt = build_prompt(idea)
        raw_response = generate_script(prompt, config)
        final_output = parse_response(raw_response)
        display_result(final_output)
        return 0
    except AppError as exc:
        display_error(str(exc))
        return 1
    except KeyboardInterrupt:
        display_error("Execucao interrompida pelo usuario.")
        return 130


if __name__ == "__main__":
    sys.exit(run())