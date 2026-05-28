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


def extrair_pais(localizacao):
    partes = str(localizacao).split(",")
    return partes[-1].strip()


def limpar_dataset(df):
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
    return df[
        df["Source Port"].between(1, 65535)
        & df["Destination Port"].between(1, 65535)
        & (df["Packet Length"] > 0)
        & df["Anomaly Scores"].between(0, 100)
        & df["Source IP Address"].map(ip_valido)
        & df["Destination IP Address"].map(ip_valido)
    ].copy()


def carregar_dados_limpos():
    if CLEAN_CSV_PATH.exists():
        df = pd.read_csv(CLEAN_CSV_PATH)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
        return df.dropna(subset=["Timestamp"])

    df = pd.read_csv(CSV_PATH)
    df = limpar_dataset(df)
    df.to_csv(CLEAN_CSV_PATH, index=False)
    return df


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


def main():
    df = carregar_dados_limpos()
    top_10, data_inicial, data_final = top_10_ddos_ultimo_mes(df)

    print("=== TOP 10 DDoS NO ULTIMO MES POR PAIS ===")
    print(f"Periodo: {data_inicial:%Y-%m-%d %H:%M:%S} ate {data_final:%Y-%m-%d %H:%M:%S}")
    print(top_10.to_string(index=False))


if __name__ == "__main__":
    main()
