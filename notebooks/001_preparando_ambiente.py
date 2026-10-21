# Databricks notebook source
# MAGIC %md
# MAGIC # 001 - Preparando o ambiente
# MAGIC
# MAGIC ### (database/schema) catalogo.schema
# MAGIC ### (volume) catalogo.schema.volume
# MAGIC
# MAGIC Cria os schemas/databases das camadas e o volume `dados` da landing.
# MAGIC
# MAGIC O banco de dados de **origem** (`LojaDB`) **não** fica no Databricks: é um PostgreSQL externo, na nuvem, criado com o script `sql/lojadb_postgres.sql`. O Databricks apenas extrai os dados dele no notebook `002`.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS workspace.landing
# MAGIC COMMENT 'Schema/Database para dados brutos (landing)';
# MAGIC
# MAGIC CREATE VOLUME IF NOT EXISTS workspace.landing.dados
# MAGIC COMMENT 'Volume para dados brutos criados no schema/database landing';
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS workspace.bronze
# MAGIC COMMENT 'Schema/Database para dados bronze (delta)';
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS workspace.silver
# MAGIC COMMENT 'Schema/Database para dados silver (delta)';
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS workspace.gold
# MAGIC COMMENT 'Schema/Database para dados gold (delta) - modelagem dimensional';

# COMMAND ----------

# MAGIC %md
# MAGIC ## (SQL) SHOW SCHEMAS IN catalogo;
# MAGIC
# MAGIC Confirmando o que foi criado.

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW SCHEMAS IN workspace;
