import logging
import os
from pathlib import Path
from typing import Optional

import pandas as pd
from dotenv import load_dotenv

# Tenta carregar variáveis do .env
load_dotenv(dotenv_path=Path(".env"))

# Usa defeaults se não houver .env
INPUT_FILE = Path(os.getenv("INPUT_CSV", "data/clientes.csv"))
OUTPUT_FILE = Path(os.getenv("OUTPUT_CSV", "output/clientes_processados.csv"))

# Carrega chave da OpenAI; se vazia, IA fica desativada
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")


def extract(input_file: Path) -> pd.DataFrame:
    logging.info("ETL: Iniciando extração...")
    df = pd.read_csv(input_file)
    logging.info("Dados extraídos com sucesso: %s linhas.", len(df))
    return df


def criar_mensagem_manual(nome: str, cidade: str, produto: str, valor: float) -> str:
    return f"Olá {nome} de {cidade}! Obrigado por comprar {produto} por R${valor:.2f}."


# Se quiser, você pode remover o 'typing.Optional' e usar só 'str' depois
def criar_mensagem_com_ia_openai(
    nome: str, cidade: str, produto: str, valor: float,
    model: str = "gpt-3.5-turbo"   # ou "gpt-4o-mini"
) -> Optional[str]:
    """
    Gera mensagem personalizada usando OpenAI.
    Se a chave não estiver definida, retorna None.
    """
    if not OPENAI_API_KEY:
        return None

    try:
        import openai
        from openai import OpenAI

        client = OpenAI(api_key=OPENAI_API_KEY)

        prompt = (
            f"Você é um assistente de marketing. "
            f"Escreva uma mensagem de agradecimento em português, bem curta e amigável, para um cliente chamado '{nome}' "
            f"que mora em '{cidade}', comprou '{produto}' por R${valor:.2f}."
        )

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Você é um assistente útil e amigável, que escreve respostas em português bem simples."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )

        mensagem = response.choices[0].message.content.strip()
        logging.info("Mensagem gerada pela IA para %s.", nome)
        return mensagem

    except Exception as e:
        logging.warning("Erro ao chamar API OpenAI (usando mensagem manual): %s", str(e))
        return None


def transform(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("ETL: Transformando dados...")
    df_transformado = df.copy()
    df_transformado["mensagem_manual"] = df_transformado.apply(
        lambda row: criar_mensagem_manual(
            row["nome"],
            row["cidade"],
            row["produto"],
            row["valor"]
        ),
        axis=1,
    )

    msgs_ia = []
    for _, row in df_transformado.iterrows():
        msg_ia = criar_mensagem_com_ia_openai(
            nome=row["nome"],
            cidade=row["cidade"],
            produto=row["produto"],
            valor=row["valor"]
        )
        msgs_ia.append(msg_ia or row["mensagem_manual"])  # usa o manual como fallback

    df_transformado["mensagem"] = msgs_ia
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