import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


MODEL = "gemini-2.5-flash"

GREEN = "\033[92m"
WHITE = "\033[97m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

SYSTEM_PROMPT = """
Voce e o cyber.ia, um assistente de seguranca cibernetica.
Responda em portugues do Brasil, com clareza e objetividade.
Ajude com conceitos, boas praticas, defesa, analise de riscos,
hardening, resposta a incidentes e aprendizado etico.
Recuse pedidos de invasao, roubo de credenciais, malware ofensivo,
exploracao nao autorizada ou qualquer dano a terceiros.
Quando recusar, ofereca uma alternativa segura e educacional.
""".strip()


def load_api_key() -> str:
    env_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(env_path)

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY nao encontrada. Crie um arquivo .env com sua chave."
        )

    return api_key


def get_token_count(response: types.GenerateContentResponse) -> tuple[int, int, int]:
    usage = response.usage_metadata
    if not usage:
        return 0, 0, 0

    prompt_tokens = usage.prompt_token_count or 0
    output_tokens = usage.candidates_token_count or 0
    total_tokens = usage.total_token_count or prompt_tokens + output_tokens
    return prompt_tokens, output_tokens, total_tokens


def main() -> None:
    os.system("")

    client = genai.Client(api_key=load_api_key())
    chat = client.chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.6,
        ),
    )

    total_spent_tokens = 0

    print(f"{CYAN}cyber.ia iniciado. Digite 'sair' para encerrar.{RESET}\n")

    while True:
        user_message = input(f"{WHITE}usuario> {RESET}").strip()

        if user_message.lower() in {"sair", "exit", "quit"}:
            print(f"{CYAN}Encerrado. Tokens totais gastos: {total_spent_tokens}{RESET}")
            break

        if not user_message:
            continue

        try:
            response = chat.send_message(user_message)
        except Exception as error:
            print(f"{YELLOW}Erro ao chamar Gemini: {error}{RESET}")
            continue

        prompt_tokens, output_tokens, turn_tokens = get_token_count(response)
        total_spent_tokens += turn_tokens

        print(f"\n{GREEN}cyber.ia> {response.text}{RESET}")
        print(
            f"{CYAN}tokens: entrada={prompt_tokens}, "
            f"saida={output_tokens}, turno={turn_tokens}, "
            f"total={total_spent_tokens}{RESET}\n"
        )


if __name__ == "__main__":
    main()
