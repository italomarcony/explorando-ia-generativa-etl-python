import logging
from pathlib import Path

import pandas as pd

INPUT_FILE = Path("data") / "clientes.csv"
OUTPUT_DIR = Path("output")
OUTPUT_FILE = OUTPUT_DIR / "clientes_processados.csv"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s"
)


def extract(input_file: Path) -> pd.DataFrame:
    logging.info("ETL: Iniciando extração...")
    df = pd.read_csv(input_file)
    logging.info("Dados extraídos com sucesso: %s linhas.", len(df))
    return df


def criar_mensagem(nome: str, cidade: str, produto: str, valor: float) -> str:
    return f"Olá {nome} de {cidade}! Obrigado por comprar {produto} por R${valor:.2f}."


def transform(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("ETL: Transformando dados...")
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
    logging.info("Transformação concluída com sucesso.")
    return df_transformado


def load(df: pd.DataFrame, output_file: Path) -> None:
    logging.info("ETL: Salvando arquivo de saída...")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False, encoding="utf-8")
    logging.info("Arquivo salvo com sucesso em: %s", output_file.absolute())


def main() -> None:
    try:
        df_extraido = extract(INPUT_FILE)
        df_transformado = transform(df_extraido)
        load(df_transformado, OUTPUT_FILE)
        logging.info("ETL finalizado com sucesso.")
    except FileNotFoundError:
        logging.error("Arquivo de entrada não encontrado: %s", INPUT_FILE)
    except pd.errors.EmptyDataError:
        logging.error("O arquivo CSV está vazio: %s", INPUT_FILE)
    except Exception as error:
        logging.exception("Erro inesperado durante o pipeline: %s", error)


if __name__ == "__main__":
    main()