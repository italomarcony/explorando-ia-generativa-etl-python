import pandas as pd
from pathlib import Path

INPUT_FILE = Path("data") / "clientes.csv"
OUTPUT_DIR = Path("output")
OUTPUT_FILE = OUTPUT_DIR / "clientes_processados.csv"


def extract(input_file: Path) -> pd.DataFrame:
    print("ETL: Iniciando extração...")
    df = pd.read_csv(input_file)
    print("Dados originais:")
    print(df.head())
    return df


def criar_mensagem(nome: str, cidade: str, produto: str, valor: float) -> str:
    return f"Olá {nome} de {cidade}! Obrigado por comprar {produto} por R${valor:.2f}."


def transform(df: pd.DataFrame) -> pd.DataFrame:
    print("\nETL: Transformando dados...")
    df_transformado = df.copy()
    df_transformado["mensagem"] = df_transformado.apply(
        lambda row: criar_mensagem(
            row["nome"],
            row["cidade"],
            row["produto"],
            row["valor"],
        ),
        axis=1,
    )
    print("Dados transformados (primeiras linhas):")
    print(df_transformado.head())
    return df_transformado


def load(df: pd.DataFrame, output_file: Path) -> None:
    print("\nETL: Salvando em CSV...")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False, encoding="utf-8")
    print("ETL: Concluído!")
    print(f"Arquivo de saída criado em: {output_file.absolute()}")


def main() -> None:
    df_extraido = extract(INPUT_FILE)
    df_transformado = transform(df_extraido)
    load(df_transformado, OUTPUT_FILE)


if __name__ == "__main__":
    main()