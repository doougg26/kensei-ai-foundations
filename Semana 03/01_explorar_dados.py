from pathlib import Path

import pandas as pd


CSV_PATH = Path(__file__).with_name("cybersecurity_attacks.csv")


def main():
    df = pd.read_csv(CSV_PATH)

    print("=== PRIMEIRAS LINHAS ===")
    print(df.head())

    print("\n=== INFO ===")
    df.info()

    print("\n=== ESTATISTICAS NUMERICAS ===")
    print(df.describe())

    print("\n=== ESTATISTICAS CATEGORICAS ===")
    print(df.describe(include="str"))

    print("\n=== VALORES NULOS ===")
    print(df.isna().sum())

    print("\n=== DUPLICADOS ===")
    print(df.duplicated().sum())


if __name__ == "__main__":
    main()
