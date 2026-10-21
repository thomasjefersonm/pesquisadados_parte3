# Databricks notebook source
# MAGIC %md
# MAGIC # 002 - Extração: Banco de dados externo (PostgreSQL) → LANDING/DADOS
# MAGIC
# MAGIC Conecta (driver `pg8000`, com SSL) no banco relacional de origem `LojaDB`, um **PostgreSQL hospedado fora do Databricks** (Supabase/Neon), extrai **todas as tabelas** e grava cada uma no formato **CSV** no volume `workspace.landing.dados`.

# COMMAND ----------

# MAGIC %md
# MAGIC ## %pip install
# MAGIC
# MAGIC Instala o `pg8000`, driver do PostgreSQL 100% Python.

# COMMAND ----------

# MAGIC %pip install pg8000

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

import ssl
import pg8000.dbapi
import pandas as pd

# SSL obrigatório (equivale ao sslmode=require)
contexto_ssl = ssl.create_default_context()
contexto_ssl.check_hostname = False
contexto_ssl.verify_mode = ssl.CERT_NONE

conexao = pg8000.dbapi.connect(
    host=conexao_params["host"],
    port=conexao_params["port"],
    database=conexao_params["dbname"],
    user=conexao_params["user"],
    password=conexao_params["password"],
    ssl_context=contexto_ssl,
    timeout=20,
)

cursor = conexao.cursor()
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
    cursor.execute(f'SELECT * FROM "{schema_origem}"."{tabela}"')
    colunas = [c[0] for c in cursor.description]
    df = pd.DataFrame(cursor.fetchall(), columns=colunas)
    df.to_csv(f"{caminho_landing}/{tabela}.csv", index=False)
    print(f"{tabela}.csv: {len(df)} linhas")

cursor.close()
conexao.close()

# COMMAND ----------

# MAGIC %md
# MAGIC ## display(dbutils.fs.ls('caminho'))
# MAGIC
# MAGIC Mostra os arquivos gravados no volume `dados`.

# COMMAND ----------

display(dbutils.fs.ls(caminho_landing))
