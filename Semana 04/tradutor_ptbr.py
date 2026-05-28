import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


MODEL = "gemini-2.5-flash"

DEFAULT_GLOSSARY = [
    "phishing",
    "malware",
    "ransomware",
    "spyware",
    "adware",
    "rootkit",
    "botnet",
    "firewall",
    "endpoint",
    "payload",
    "exploit",
    "zero-day",
    "backdoor",
    "honeypot",
    "SOC",
    "SIEM",
    "EDR",
    "XDR",
    "DDoS",
    "IoC",
    "hash",
    "token",
    "API",
    "backup",
    "hardening",
    "pentest",
]

SYSTEM_PROMPT = """
Voce e um tradutor profissional especializado em tecnologia e ciberseguranca.
Detecte automaticamente o idioma do texto de entrada e traduza para portugues do Brasil.
Preserve o significado, o tom e a estrutura quando fizer sentido.
Nao traduza termos do glossario. Mantenha siglas e nomes de tecnologias.
Responda somente com o texto traduzido, sem explicacoes.
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


def build_glossary(extra_terms: list[str]) -> list[str]:
    glossary = DEFAULT_GLOSSARY.copy()

    for term in extra_terms:
        clean_term = term.strip()
        if clean_term and clean_term not in glossary:
            glossary.append(clean_term)

    return glossary


def translate_text(client: genai.Client, text: str, glossary: list[str]) -> str:
    glossary_text = ", ".join(glossary)
    prompt = f"""
Traduza o texto abaixo para pt-BR.

Termos do glossario que nao devem ser traduzidos:
{glossary_text}

Texto:
{text}
""".strip()

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.2,
        ),
    )

    return response.text.strip()


def output_path_for_txt(path: Path) -> Path:
    return path.with_name(f"{path.stem}_pt{path.suffix}")


def collect_txt_files(input_path: Path) -> list[Path]:
    if input_path.is_file():
        if input_path.suffix.lower() != ".txt":
            raise ValueError("O arquivo precisa ter extensao .txt.")
        return [input_path]

    if input_path.is_dir():
        return sorted(
            path
            for path in input_path.rglob("*.txt")
            if path.is_file() and not path.stem.endswith("_pt")
        )

    raise FileNotFoundError(f"Caminho nao encontrado: {input_path}")


def translate_file(client: genai.Client, path: Path, glossary: list[str]) -> Path:
    text = path.read_text(encoding="utf-8")
    translated = translate_text(client, text, glossary)

    output_path = output_path_for_txt(path)
    output_path.write_text(translated, encoding="utf-8")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Detecta o idioma e traduz texto, arquivo ou pasta de .txt para pt-BR."
    )
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        "-t",
        "--texto",
        help="Texto direto para traduzir.",
    )
    input_group.add_argument(
        "-a",
        "--arquivo",
        help="Arquivo .txt para traduzir. Padrao sem argumentos: texto.txt",
    )
    input_group.add_argument(
        "-p",
        "--pasta",
        help="Pasta com arquivos .txt para traduzir em lote.",
    )
    parser.add_argument(
        "-g",
        "--glossario",
        action="append",
        default=[],
        help="Termo tecnico extra que nao deve ser traduzido. Pode repetir a opcao.",
    )
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent
    client = genai.Client(api_key=load_api_key())
    glossary = build_glossary(args.glossario)

    if args.texto:
        translated = translate_text(client, args.texto, glossary)
        print(translated)
        return

    input_path = Path(args.arquivo or args.pasta or "texto.txt")
    if not input_path.is_absolute():
        input_path = base_dir / input_path

    txt_files = collect_txt_files(input_path)

    if not txt_files:
        raise RuntimeError("Nenhum arquivo .txt encontrado para traduzir.")

    for txt_file in txt_files:
        output_path = translate_file(client, txt_file, glossary)
        print(f"Traduzido: {txt_file} -> {output_path}")


if __name__ == "__main__":
    main()
