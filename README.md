# Explorando IA Generativa em um Pipeline de ETL com Python

Projeto de portfólio focado na construção de um pipeline ETL em Python.

## Objetivo
Ler uma base CSV de clientes, transformar os dados gerando mensagens personalizadas e salvar o resultado em um novo CSV.

## Estrutura do projeto
- `data/`: dados de entrada
- `output/`: arquivos gerados pelo pipeline
- `src/`: código-fonte do projeto
- `requirements.txt`: dependências do projeto

## Tecnologias
- Python
- pandas

## Etapas do pipeline
- Extract: leitura de CSV local
- Transform: geração de mensagem personalizada por cliente
- Load: exportação para novo CSV

## Como executar
```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
python src/etl.py
```