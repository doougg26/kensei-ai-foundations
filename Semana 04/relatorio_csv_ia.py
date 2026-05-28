import argparse
import json
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai import types


BASE_DIR = Path(__file__).resolve().parent
MODEL = "gemini-2.5-flash"

os.environ.setdefault("MPLCONFIGDIR", str(BASE_DIR / ".matplotlib_cache"))

import matplotlib.pyplot as plt  # noqa: E402


SYSTEM_PROMPT = """
Voce e um analista senior de dados.
Crie um relatorio executivo em Markdown, em portugues do Brasil.
Use linguagem clara, objetiva e orientada a decisao.
Nao invente dados que nao estejam no resumo recebido.
Inclua referencias aos graficos usando os caminhos informados.
""".strip()


def to_json_safe(value):
    if isinstance(value, dict):
        return {str(key): to_json_safe(item) for key, item in value.items()}

    if isinstance(value, list):
        return [to_json_safe(item) for item in value]

    if pd.isna(value):
        return None

    if hasattr(value, "item"):
        return value.item()

    return value


def load_api_key() -> str:
    env_path = BASE_DIR / ".env"
    load_dotenv(env_path)

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY nao encontrada. Crie um arquivo .env com sua chave."
        )

    return api_key


def read_csv(path: Path) -> pd.DataFrame:
    for encoding in ("utf-8", "utf-8-sig", "latin1"):
        try:
            return pd.read_csv(path, encoding=encoding, low_memory=False)
        except UnicodeDecodeError:
            continue

    return pd.read_csv(path, low_memory=False)


def clean_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()

    for column in cleaned.columns:
        if pd.api.types.is_numeric_dtype(cleaned[column]):
            continue

        sample = cleaned[column].dropna().astype(str).head(50)
        if sample.empty:
            continue

        numeric_like = sample.str.contains(r"\d", regex=True).mean()
        currency_like = sample.str.contains("$", regex=False).mean()

        if numeric_like >= 0.7 and currency_like >= 0.3:
            converted = (
                cleaned[column]
                .astype(str)
                .str.replace(r"[^0-9,.-]", "", regex=True)
                .str.replace(",", "", regex=False)
            )
            cleaned[f"{column}_num"] = pd.to_numeric(converted, errors="coerce")

    return cleaned


def get_basic_profile(df: pd.DataFrame) -> dict:
    numeric_columns = df.select_dtypes(include="number").columns.tolist()
    categorical_columns = df.select_dtypes(exclude="number").columns.tolist()

    missing = (
        df.isna()
        .sum()
        .sort_values(ascending=False)
        .head(15)
        .to_dict()
    )

    numeric_summary = (
        df[numeric_columns]
        .describe()
        .round(2)
        .to_dict()
        if numeric_columns
        else {}
    )

    categorical_summary = {}
    for column in categorical_columns[:10]:
        categorical_summary[column] = (
            df[column]
            .dropna()
            .astype(str)
            .value_counts()
            .head(10)
            .to_dict()
        )

    return to_json_safe(
        {
            "linhas": int(df.shape[0]),
            "colunas": int(df.shape[1]),
            "nomes_colunas": df.columns.tolist(),
            "colunas_numericas": numeric_columns,
            "colunas_categoricas": categorical_columns,
            "valores_ausentes_top15": missing,
            "resumo_numerico": numeric_summary,
            "frequencias_categoricas_top10": categorical_summary,
        }
    )


def save_missing_chart(df: pd.DataFrame, output_dir: Path) -> Path | None:
    missing = df.isna().sum().sort_values(ascending=False)
    missing = missing[missing > 0].head(10)

    if missing.empty:
        return None

    path = output_dir / "grafico_valores_ausentes.png"
    plt.figure(figsize=(10, 5))
    missing.sort_values().plot(kind="barh", color="#455a64")
    plt.title("Top 10 colunas com valores ausentes")
    plt.xlabel("Quantidade")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def save_numeric_chart(df: pd.DataFrame, output_dir: Path) -> Path | None:
    numeric_columns = df.select_dtypes(include="number").columns.tolist()
    if not numeric_columns:
        return None

    column = numeric_columns[0]
    series = df[column].dropna()
    if series.empty:
        return None

    path = output_dir / f"grafico_distribuicao_{column}.png"
    plt.figure(figsize=(10, 5))
    series.plot(kind="hist", bins=30, color="#2e7d32", edgecolor="white")
    plt.title(f"Distribuicao de {column}")
    plt.xlabel(column)
    plt.ylabel("Frequencia")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def save_categorical_chart(df: pd.DataFrame, output_dir: Path) -> Path | None:
    categorical_columns = df.select_dtypes(exclude="number").columns.tolist()

    for column in categorical_columns:
        counts = df[column].dropna().astype(str).value_counts().head(10)
        if len(counts) >= 2:
            safe_column = "".join(
                char if char.isalnum() or char in ("-", "_") else "_"
                for char in column
            )
            path = output_dir / f"grafico_top10_{safe_column}.png"
            plt.figure(figsize=(10, 5))
            counts.sort_values().plot(kind="barh", color="#1565c0")
            plt.title(f"Top 10 categorias em {column}")
            plt.xlabel("Quantidade")
            plt.tight_layout()
            plt.savefig(path, dpi=150)
            plt.close()
            return path

    return None


def create_charts(df: pd.DataFrame, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)

    charts = [
        save_missing_chart(df, output_dir),
        save_numeric_chart(df, output_dir),
        save_categorical_chart(df, output_dir),
    ]

    return [chart for chart in charts if chart is not None]


def build_prompt(csv_path: Path, profile: dict, charts: list[Path]) -> str:
    chart_refs = "\n".join(f"- {chart.as_posix()}" for chart in charts)
    profile_json = json.dumps(profile, ensure_ascii=False, indent=2)

    return f"""
Gere um relatorio executivo em Markdown para o CSV abaixo.

Arquivo analisado: {csv_path}

Resumo tecnico dos dados:
```json
{profile_json}
```

Graficos gerados e que devem ser referenciados no Markdown:
{chart_refs or "- Nenhum grafico gerado"}

Estrutura desejada:
1. Titulo
2. Sumario executivo
3. Visao geral dos dados
4. Principais achados
5. Leitura dos graficos
6. Riscos ou limitacoes da analise
7. Recomendacoes executivas

Inclua imagens no Markdown usando a sintaxe:
![descricao](caminho/do/grafico.png)
""".strip()


def generate_report(client: genai.Client, prompt: str) -> str:
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.4,
        ),
    )

    return response.text.strip()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Carrega um CSV, analisa com Pandas e gera relatorio executivo com IA."
    )
    parser.add_argument(
        "csv",
        nargs="?",
        default="steam_games.csv",
        help="Caminho do CSV. Padrao: steam_games.csv",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="relatorio_executivo.md",
        help="Arquivo Markdown de saida. Padrao: relatorio_executivo.md",
    )
    parser.add_argument(
        "--charts-dir",
        default="graficos_relatorio",
        help="Pasta para salvar graficos. Padrao: graficos_relatorio",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv)
    output_path = Path(args.output)
    charts_dir = Path(args.charts_dir)

    if not csv_path.is_absolute():
        csv_path = BASE_DIR / csv_path
    if not output_path.is_absolute():
        output_path = BASE_DIR / output_path
    if not charts_dir.is_absolute():
        charts_dir = BASE_DIR / charts_dir

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV nao encontrado: {csv_path}")

    print(f"Carregando CSV: {csv_path}")
    df = read_csv(csv_path)
    df = clean_numeric_columns(df)

    print("Analisando dados com Pandas...")
    profile = get_basic_profile(df)

    print("Gerando graficos...")
    charts = create_charts(df, charts_dir)

    print("Gerando relatorio executivo com Gemini...")
    client = genai.Client(api_key=load_api_key())
    prompt = build_prompt(csv_path, profile, charts)
    report = generate_report(client, prompt)

    output_path.write_text(report, encoding="utf-8")
    print(f"\nRelatorio salvo em: {output_path}")

    if charts:
        print("Graficos gerados:")
        for chart in charts:
            print(f"- {chart}")


if __name__ == "__main__":
    main()
