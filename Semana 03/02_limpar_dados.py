from ipaddress import ip_address
from pathlib import Path

import pandas as pd


CSV_PATH = Path(__file__).with_name("cybersecurity_attacks.csv")
CLEAN_CSV_PATH = Path(__file__).with_name("cybersecurity_attacks_limpo.csv")


def ip_valido(valor):
    try:
        ip_address(str(valor))
        return True
    except ValueError:
        return False


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

    relatorio = {
        "linhas_iniciais": linhas_iniciais,
        "linhas_finais": len(df),
        "linhas_removidas": linhas_iniciais - len(df),
        "duplicados_removidos": duplicados_removidos,
        "nulos_preenchidos": nulos_preenchidos,
    }

    return df, relatorio


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


if __name__ == "__main__":
    main()
