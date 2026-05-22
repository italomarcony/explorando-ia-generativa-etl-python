# src/etl.py
import pandas as pd
from pathlib import Path

# Caminhos relativos
INPUT_FILE = Path("data") / "clientes.csv"
OUTPUT_DIR = Path("output")
OUTPUT_FILE = OUTPUT_DIR / "clientes_processados.csv"

def main():
    print("ETL: Iniciando extração...")
    # Extract
    df = pd.read_csv(INPUT_FILE)
    print("Dados originais:")
    print(df.head())

    # Transform
    print("\nETL: Transformando dados...")
    df["mensagem"] = df.apply(
        lambda row: (
            f"Olá {row['nome']} de {row['cidade']}!"
            f" Obrigado por comprar {row['produto']} por R${row['valor']:.2f}."
        ),
        axis=1,
    )
    print("Dados transformados (primeiras linhas):")
    print(df.head())

    # Load
    print("\nETL: Salvando em CSV...")
    OUTPUT_DIR.mkdir(exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    print("ETL: Concluído!")
    print(f"Arquivo de saída criado em: {OUTPUT_FILE.absolute()}")


if __name__ == "__main__":
    main()