# Databricks notebook source
# MAGIC %md
# MAGIC # 002 - Extração: Banco de dados externo (PostgreSQL) → LANDING/DADOS
# MAGIC
# MAGIC Conecta no banco relacional de origem `LojaDB`, um **PostgreSQL hospedado fora do Databricks** (Supabase/Neon), extrai **todas as tabelas** e grava cada uma no formato **CSV** no volume `workspace.landing.dados`.

# COMMAND ----------

# MAGIC %md
# MAGIC ## %pip install
# MAGIC
# MAGIC Instala o driver do PostgreSQL para Python.

# COMMAND ----------

# MAGIC %pip install psycopg2-binary

# COMMAND ----------

# MAGIC %md
# MAGIC ## Parâmetros de conexão
# MAGIC
# MAGIC Os dados de conexão chegam como **parâmetros** (widgets do notebook / parâmetros do Job), para que a senha **não** fique gravada no GitHub.

# COMMAND ----------

dbutils.widgets.text("pg_host", "")
dbutils.widgets.text("pg_port", "5432")
dbutils.widgets.text("pg_database", "postgres")
dbutils.widgets.text("pg_user", "")
dbutils.widgets.text("pg_password", "")
dbutils.widgets.text("pg_schema", "public")

conexao_params = {
    "host":     dbutils.widgets.get("pg_host"),
    "port":     int(dbutils.widgets.get("pg_port")),
    "dbname":   dbutils.widgets.get("pg_database"),
    "user":     dbutils.widgets.get("pg_user"),
    "password": dbutils.widgets.get("pg_password"),
    "sslmode":  "require",
}
schema_origem = dbutils.widgets.get("pg_schema")
caminho_landing = '/Volumes/workspace/landing/dados'

assert conexao_params["host"] and conexao_params["password"], "Preencha os parâmetros pg_host / pg_user / pg_password"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Lista todas as tabelas do banco de origem
# MAGIC
# MAGIC Consulta o catálogo do próprio PostgreSQL (`information_schema.tables`). Como a lista vem do banco, novas tabelas também são extraídas sem alterar o código.

# COMMAND ----------

import psycopg2
import pandas as pd

conexao = psycopg2.connect(**conexao_params)

with conexao.cursor() as cursor:
    cursor.execute(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = %s AND table_type = 'BASE TABLE'
        ORDER BY table_name
        """,
        (schema_origem,),
    )
    tabelas = [linha[0] for linha in cursor.fetchall()]

print(tabelas)

# COMMAND ----------

# MAGIC %md
# MAGIC ## SELECT * → df.to_csv("path + filename")
# MAGIC
# MAGIC Lê cada tabela do banco externo e grava um arquivo CSV por tabela no volume `dados` (`clientes.csv`, `pedidos.csv`).

# COMMAND ----------

for tabela in tabelas:
    with conexao.cursor() as cursor:
        cursor.execute(f'SELECT * FROM "{schema_origem}"."{tabela}"')
        colunas = [c[0] for c in cursor.description]
        df = pd.DataFrame(cursor.fetchall(), columns=colunas)
    df.to_csv(f"{caminho_landing}/{tabela}.csv", index=False)
    print(f"{tabela}.csv: {len(df)} linhas")

conexao.close()

# COMMAND ----------

# MAGIC %md
# MAGIC ## display(dbutils.fs.ls('caminho'))
# MAGIC
# MAGIC Mostra os arquivos gravados no volume `dados`.

# COMMAND ----------

display(dbutils.fs.ls(caminho_landing))
