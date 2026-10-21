# Databricks notebook source
# MAGIC %md
# MAGIC # 003 - Ingestão: LANDING/DADOS → BRONZE
# MAGIC
# MAGIC ## display(dbutils.fs.ls('caminho'))
# MAGIC
# MAGIC Mostra todos os arquivos que estão dentro do Volume "dados" do schema/database landing.

# COMMAND ----------

display(dbutils.fs.ls('/Volumes/workspace/landing/dados/'))

# COMMAND ----------

# MAGIC %md
# MAGIC ## df = spark.read.option("inferSchema", "true").option("header", "true").csv("path + filename")
# MAGIC
# MAGIC Gera um dataframe para cada arquivo que está no Volume "dados".

# COMMAND ----------

caminho_landing = '/Volumes/workspace/landing/dados'

df_clientes = spark.read.option("inferSchema", "true").option("header", "true").csv(f"{caminho_landing}/clientes.csv")
df_pedidos  = spark.read.option("inferSchema", "true").option("header", "true").csv(f"{caminho_landing}/pedidos.csv")

# COMMAND ----------

# MAGIC %md
# MAGIC ## df = df.withColumn("nome_coluna", "valor")
# MAGIC
# MAGIC Adiciona uma nova coluna (metadado) de data e hora de processamento e nome do arquivo de origem.

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit

df_clientes = df_clientes.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("clientes.csv"))
df_pedidos  = df_pedidos.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("pedidos.csv"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## df.write.format('delta').saveAsTable("nome_tabela")
# MAGIC
# MAGIC Salva os dataframes no formato delta lake no schema/database "bronze". As tabelas geradas são do tipo MANAGED (gerenciadas).

# COMMAND ----------

df_clientes.write.format('delta').mode("overwrite").saveAsTable("bronze.clientes")
df_pedidos.write.format('delta').mode("overwrite").saveAsTable("bronze.pedidos")

# COMMAND ----------

# MAGIC %md
# MAGIC ## (SQL) SHOW TABLES IN bronze
# MAGIC
# MAGIC Verifica os dados gravados no formato delta lake tipo MANAGED na camada bronze.

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN bronze

# COMMAND ----------

# MAGIC %md
# MAGIC ## (SQL) DESCRIBE DETAIL nome_tabela;
# MAGIC
# MAGIC Vendo os detalhes de uma tabela delta lake.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL bronze.pedidos;

# COMMAND ----------

# MAGIC %md
# MAGIC ## (SQL) DESCRIBE EXTENDED nome_tabela;
# MAGIC
# MAGIC Mostra se a tabela é MANAGED ou EXTERNAL.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED bronze.pedidos;
