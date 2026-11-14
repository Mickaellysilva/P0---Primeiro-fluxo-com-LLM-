from src.exceptions import InputValidationError


def capture_input() -> str:
    user_input = input("Digite a ideia do post ou video curto: ").strip()
    if not user_input:
        raise InputValidationError(
            "Entrada invalida: o texto nao pode estar vazio. Informe uma ideia para gerar o roteiro."
        )
    return user_input


def display_result(result: str) -> None:
    print("\n--- ROTEIRO GERADO ---\n")
    print(result)


def display_error(message: str) -> None:
    print(f"\n[ERRO] {message}")