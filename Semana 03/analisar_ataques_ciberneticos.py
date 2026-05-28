from pathlib import Path
from ipaddress import ip_address
import os

CSV_PATH = Path(__file__).with_name("cybersecurity_attacks.csv")
CLEAN_CSV_PATH = Path(__file__).with_name("cybersecurity_attacks_limpo.csv")
TOP_10_PAISES_PNG = Path(__file__).with_name("grafico_top_10_paises.png")
ATAQUES_POR_MES_PNG = Path(__file__).with_name("grafico_ataques_por_mes.png")
TIPOS_ATAQUE_PNG = Path(__file__).with_name("grafico_tipos_ataque.png")
MATPLOTLIB_CONFIG_DIR = Path(__file__).with_name(".matplotlib")

os.environ.setdefault("MPLCONFIGDIR", str(MATPLOTLIB_CONFIG_DIR))

import matplotlib.pyplot as plt
import pandas as pd


def ip_valido(valor):
    try:
        ip_address(str(valor))
        return True
    except ValueError:
        return False


def extrair_pais(localizacao):
    partes = str(localizacao).split(",")
    return partes[-1].strip()


def limpar_dataset(df):
    linhas_iniciais = len(df)
    duplicados_removidos = df.duplicated().sum()
    nulos_preenchidos = df.isna().sum().sum()

    df = df.drop_duplicates()

    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    df = df.dropna(subset=["Timestamp"])

    colunas_texto = df.select_dtypes(include="str").columns
    df[colunas_texto] = df[colunas_texto].fillna("Nao informado")

    colunas_numericas = [
        "Source Port",
        "Destination Port",
        "Packet Length",
        "Anomaly Scores",
    ]
    for coluna in colunas_numericas:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    df = df.dropna(subset=colunas_numericas)
    df = df[
        df["Source Port"].between(1, 65535)
        & df["Destination Port"].between(1, 65535)
        & (df["Packet Length"] > 0)
        & df["Anomaly Scores"].between(0, 100)
        & df["Source IP Address"].map(ip_valido)
        & df["Destination IP Address"].map(ip_valido)
    ].copy()

    linhas_finais = len(df)
    relatorio = {
        "linhas_iniciais": linhas_iniciais,
        "linhas_finais": linhas_finais,
        "linhas_removidas": linhas_iniciais - linhas_finais,
        "duplicados_removidos": duplicados_removidos,
        "nulos_preenchidos": nulos_preenchidos,
    }

    return df, relatorio


def top_10_ddos_ultimo_mes(df):
    data_final = df["Timestamp"].max()
    data_inicial = data_final - pd.DateOffset(months=1)

    ddos_ultimo_mes = df[
        (df["Attack Type"].str.upper() == "DDOS")
        & (df["Timestamp"] >= data_inicial)
        & (df["Timestamp"] <= data_final)
    ].copy()

    ddos_ultimo_mes["Pais"] = ddos_ultimo_mes["Geo-location Data"].map(extrair_pais)

    top_10 = (
        ddos_ultimo_mes.groupby("Pais")
        .size()
        .reset_index(name="Total de ataques")
        .sort_values("Total de ataques", ascending=False)
        .head(10)
    )

    return top_10, data_inicial, data_final


def salvar_graficos(df, top_10_paises):
    plt.style.use("seaborn-v0_8-whitegrid")

    plt.figure(figsize=(12, 6))
    plt.bar(top_10_paises["Pais"], top_10_paises["Total de ataques"], color="#2563eb")
    plt.title("Top 10 paises com mais ataques DDoS no ultimo mes")
    plt.xlabel("Pais")
    plt.ylabel("Total de ataques")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(TOP_10_PAISES_PNG, dpi=150)
    plt.close()

    ataques_por_mes = (
        df.set_index("Timestamp")
        .resample("ME")
        .size()
        .reset_index(name="Total de ataques")
    )
    ataques_por_mes["Mes"] = ataques_por_mes["Timestamp"].dt.strftime("%Y-%m")

    plt.figure(figsize=(12, 6))
    plt.plot(
        ataques_por_mes["Mes"],
        ataques_por_mes["Total de ataques"],
        marker="o",
        color="#16a34a",
    )
    plt.title("Ataques por mes")
    plt.xlabel("Mes")
    plt.ylabel("Total de ataques")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(ATAQUES_POR_MES_PNG, dpi=150)
    plt.close()

    tipos_ataque = df["Attack Type"].value_counts()

    plt.figure(figsize=(8, 8))
    plt.pie(
        tipos_ataque,
        labels=tipos_ataque.index,
        autopct="%1.1f%%",
        startangle=90,
    )
    plt.title("Distribuicao por tipo de ataque")
    plt.tight_layout()
    plt.savefig(TIPOS_ATAQUE_PNG, dpi=150)
    plt.close()

    return [TOP_10_PAISES_PNG, ATAQUES_POR_MES_PNG, TIPOS_ATAQUE_PNG]


def main():
    df = pd.read_csv(CSV_PATH)
    df, relatorio = limpar_dataset(df)
    df.to_csv(CLEAN_CSV_PATH, index=False)

    print("=== LIMPEZA ===")
    print(f"Linhas iniciais: {relatorio['linhas_iniciais']}")
    print(f"Linhas finais: {relatorio['linhas_finais']}")
    print(f"Linhas removidas: {relatorio['linhas_removidas']}")
    print(f"Duplicados removidos: {relatorio['duplicados_removidos']}")
    print(f"Valores nulos preenchidos: {relatorio['nulos_preenchidos']}")
    print(f"Arquivo limpo salvo em: {CLEAN_CSV_PATH}")

    print("=== PRIMEIRAS LINHAS ===")
    print(df.head())

    print("\n=== INFO ===")
    df.info()

    print("\n=== ESTATISTICAS NUMERICAS ===")
    print(df.describe())

    print("\n=== ESTATISTICAS CATEGORICAS ===")
    print(df.describe(include="str"))

    top_10, data_inicial, data_final = top_10_ddos_ultimo_mes(df)

    print("\n=== TOP 10 DDoS NO ULTIMO MES POR PAIS ===")
    print(f"Periodo: {data_inicial:%Y-%m-%d %H:%M:%S} ate {data_final:%Y-%m-%d %H:%M:%S}")
    print(top_10.to_string(index=False))

    graficos = salvar_graficos(df, top_10)

    print("\n=== GRAFICOS SALVOS ===")
    for grafico in graficos:
        print(grafico)


if __name__ == "__main__":
    main()
