import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


def main() -> None:
    env_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(env_path)

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY nao encontrada. Crie um arquivo .env com sua chave."
        )

    client = genai.Client(api_key=api_key)
    prompt = input("Digite sua pergunta para o Gemini: ").strip()

    if not prompt:
        print("Nenhuma pergunta enviada.")
        return

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    print("\nResposta do Gemini:\n")
    print(response.text)


if __name__ == "__main__":
    main()
