# Databricks notebook source
# MAGIC %md
# MAGIC # 006 - Destruindo o ambiente
# MAGIC
# MAGIC ### (database/schema) catalogo.schema
# MAGIC ### (volume) catalogo.schema.volume
# MAGIC
# MAGIC Apaga os schemas/databases, as tabelas e o volume. Não faz parte do Job.
# MAGIC
# MAGIC O banco de origem (PostgreSQL externo) **não** é apagado: ele não pertence ao Databricks.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Apagar todas as tabelas da camada bronze
# MAGIC DROP SCHEMA IF EXISTS workspace.bronze CASCADE;
# MAGIC
# MAGIC -- Apagar todas as tabelas da camada silver
# MAGIC DROP SCHEMA IF EXISTS workspace.silver CASCADE;
# MAGIC
# MAGIC -- Apagar todas as tabelas da camada gold
# MAGIC DROP SCHEMA IF EXISTS workspace.gold CASCADE;
# MAGIC
# MAGIC -- Apagar todas as tabelas e volumes da camada landing
# MAGIC DROP SCHEMA IF EXISTS workspace.landing CASCADE;

# COMMAND ----------

# MAGIC %md
# MAGIC ## (SQL) SHOW SCHEMAS IN catalogo;
# MAGIC
# MAGIC Confirmar se tudo foi limpo.

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW SCHEMAS IN workspace;
