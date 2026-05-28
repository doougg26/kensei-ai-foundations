import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


MODEL = "gemini-2.5-flash"

SYSTEM_PROMPT = """
Voce e um analisador de textos.
Para cada texto recebido, gere:
- um resumo em exatamente 3 frases;
- o sentimento geral;
- 5 palavras-chave.
Responda somente em JSON valido, sem markdown.
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


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def analyze_text(client: genai.Client, text: str) -> dict:
    prompt = f"""
Analise o texto abaixo e retorne somente este JSON:

{{
  "resumo": ["frase 1", "frase 2", "frase 3"],
  "sentimento": "positivo|neutro|negativo|misto",
  "palavras_chave": ["palavra 1", "palavra 2", "palavra 3", "palavra 4", "palavra 5"]
}}

Texto:
{text}
""".strip()

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
        ),
    )

    return json.loads(response.text)


def collect_txt_files(input_path: Path) -> list[Path]:
    if input_path.is_file():
        if input_path.suffix.lower() != ".txt":
            raise ValueError("O arquivo de entrada precisa ter extensao .txt.")
        return [input_path]

    if input_path.is_dir():
        return sorted(path for path in input_path.rglob("*.txt") if path.is_file())

    raise FileNotFoundError(
        f"Caminho nao encontrado: {input_path}\n"
        "Informe um arquivo .txt ou uma pasta. Exemplo: "
        'python analisar_textos.py texto.txt'
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analisa um arquivo .txt ou uma pasta inteira de .txt com Gemini."
    )
    parser.add_argument(
        "entrada",
        nargs="?",
        default="texto.txt",
        help="Arquivo .txt ou pasta com arquivos .txt. Padrao: texto.txt",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="analise.json",
        help="Arquivo JSON de saida. Padrao: analise.json",
    )
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent
    input_path = Path(args.entrada)
    output_path = Path(args.output)

    if not input_path.is_absolute():
        input_path = base_dir / input_path

    if not output_path.is_absolute():
        output_path = base_dir / output_path

    client = genai.Client(api_key=load_api_key())
    txt_files = collect_txt_files(input_path)

    if not txt_files:
        raise RuntimeError("Nenhum arquivo .txt encontrado para analisar.")

    results = []

    for txt_file in txt_files:
        print(f"Analisando: {txt_file}")
        text = read_text_file(txt_file)
        analysis = analyze_text(client, text)

        results.append(
            {
                "arquivo": str(txt_file),
                "analise": analysis,
            }
        )

    output_data = {
        "total_arquivos": len(results),
        "resultados": results,
    }

    output_path.write_text(
        json.dumps(output_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\nAnalise salva em: {output_path}")


if __name__ == "__main__":
    main()
