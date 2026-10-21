# Databricks notebook source
# MAGIC %md
# MAGIC # 002 - Extração: Banco de dados → LANDING/DADOS
# MAGIC
# MAGIC Extrai **todas as tabelas** do banco relacional `lojadb` e grava cada uma no formato **CSV** no volume `workspace.landing.dados`.

# COMMAND ----------

# MAGIC %md
# MAGIC ## (SQL) SHOW TABLES IN schema
# MAGIC
# MAGIC Lista todas as tabelas do banco de origem. Como a lista vem do próprio banco, novas tabelas também são extraídas.

# COMMAND ----------

caminho_landing = '/Volumes/workspace/landing/dados'

tabelas = [t.tableName for t in spark.sql("SHOW TABLES IN workspace.lojadb").collect()]
print(tabelas)

# COMMAND ----------

# MAGIC %md
# MAGIC ## df.toPandas().to_csv("path + filename")
# MAGIC
# MAGIC Grava um arquivo CSV por tabela no volume `dados` (`clientes.csv`, `pedidos.csv`).

# COMMAND ----------

for tabela in tabelas:
    df = spark.read.table(f"workspace.lojadb.{tabela}")
    df.toPandas().to_csv(f"{caminho_landing}/{tabela}.csv", index=False)
    print(f"{tabela}.csv: {df.count()} linhas")

# COMMAND ----------

# MAGIC %md
# MAGIC ## display(dbutils.fs.ls('caminho'))
# MAGIC
# MAGIC Mostra os arquivos gravados no volume `dados`.

# COMMAND ----------

display(dbutils.fs.ls(caminho_landing))
