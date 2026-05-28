from pathlib import Path
import os


CSV_PATH = Path(__file__).with_name("01_Netflix_2016_2025.csv")
GENERO_PNG = Path(__file__).with_name("netflix_generos.png")
ANOS_PNG = Path(__file__).with_name("netflix_anos.png")
TIPO_PNG = Path(__file__).with_name("netflix_tipos.png")
MATPLOTLIB_CONFIG_DIR = Path(__file__).with_name(".matplotlib")

os.environ.setdefault("MPLCONFIGDIR", str(MATPLOTLIB_CONFIG_DIR))

import matplotlib.pyplot as plt
import pandas as pd


def identificar_tipo(duracao):
    texto = str(duracao).lower()

    if "webfilm" in texto:
        return "Filme/Webfilm"
    if "eps" in texto:
        return "Minisserie/Episodios"
    if "season" in texto or texto.startswith("s"):
        return "Serie"

    return "Outro"


def salvar_graficos(df):
    plt.style.use("seaborn-v0_8-whitegrid")

    generos = df["Genre"].str.strip().value_counts().head(10)
    plt.figure(figsize=(12, 6))
    plt.bar(generos.index, generos.values, color="#e50914")
    plt.title("Top 10 generos na Netflix")
    plt.xlabel("Genero")
    plt.ylabel("Quantidade")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(GENERO_PNG, dpi=150)
    plt.close()

    anos = df["Year"].value_counts().sort_index()
    plt.figure(figsize=(10, 6))
    plt.plot(anos.index, anos.values, marker="o", color="#2563eb")
    plt.title("Titulos por ano")
    plt.xlabel("Ano")
    plt.ylabel("Quantidade")
    plt.xticks(anos.index, rotation=45)
    plt.tight_layout()
    plt.savefig(ANOS_PNG, dpi=150)
    plt.close()

    df["Tipo"] = df["Duration"].map(identificar_tipo)
    tipos = df["Tipo"].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(tipos.values, labels=tipos.index, autopct="%1.1f%%", startangle=90)
    plt.title("Distribuicao por tipo")
    plt.tight_layout()
    plt.savefig(TIPO_PNG, dpi=150)
    plt.close()

    return [GENERO_PNG, ANOS_PNG, TIPO_PNG]


def main():
    df = pd.read_csv(CSV_PATH, encoding="latin1")

    linhas_iniciais = len(df)
    duplicados = df.duplicated().sum()
    df_sem_duplicados = df.drop_duplicates()

    print("=== DATASET NETFLIX 2016-2025 ===")
    print(f"Arquivo: {CSV_PATH}")
    print(f"Linhas iniciais: {linhas_iniciais}")
    print(f"Duplicados removidos: {duplicados}")
    print(f"Linhas finais: {len(df_sem_duplicados)}")

    print("\n=== DADOS SEM DUPLICADOS ===")
    print(df_sem_duplicados.to_string(index=False))

    graficos = salvar_graficos(df_sem_duplicados)

    print("\n=== GRAFICOS SALVOS ===")
    for grafico in graficos:
        print(grafico)


if __name__ == "__main__":
    main()
