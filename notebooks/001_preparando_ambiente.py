# Databricks notebook source
# MAGIC %md
# MAGIC # 001 - Preparando o ambiente
# MAGIC
# MAGIC ### (database/schema) catalogo.schema
# MAGIC ### (volume) catalogo.schema.volume
# MAGIC
# MAGIC Cria o banco de dados relacional de origem (`lojadb`, o mesmo dos trabalhos 1 e 2), os schemas/databases das camadas e o volume `dados` da landing.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS workspace.lojadb
# MAGIC COMMENT 'Schema/Database de origem (banco relacional LojaDB)';
# MAGIC
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
# MAGIC ## Banco de dados de origem (LojaDB)
# MAGIC
# MAGIC Mesmo DDL e mesmos dados dos trabalhos 1 e 2.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.lojadb.clientes (
# MAGIC   id_cliente INT NOT NULL,
# MAGIC   nome       VARCHAR(100) NOT NULL,
# MAGIC   cidade     VARCHAR(100),
# MAGIC   uf         CHAR(2)
# MAGIC );
# MAGIC
# MAGIC INSERT INTO workspace.lojadb.clientes VALUES
# MAGIC   (1, 'Ana Souza',  'Criciúma',      'SC'),
# MAGIC   (2, 'Bruno Lima', 'Florianópolis', 'SC'),
# MAGIC   (3, 'Carla Dias', 'Porto Alegre',  'RS'),
# MAGIC   (4, 'Diego Melo', 'Curitiba',      'PR');

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.lojadb.pedidos (
# MAGIC   id_pedido      INT NOT NULL,
# MAGIC   id_cliente     INT NOT NULL,
# MAGIC   produto        VARCHAR(100) NOT NULL,
# MAGIC   quantidade     INT NOT NULL,
# MAGIC   valor_unitario DECIMAL(10,2) NOT NULL,
# MAGIC   data_pedido    DATE NOT NULL,
# MAGIC   status         VARCHAR(20) NOT NULL
# MAGIC );
# MAGIC
# MAGIC INSERT INTO workspace.lojadb.pedidos VALUES
# MAGIC   (101, 1, 'Notebook', 1, 4500.00, DATE'2026-09-01', 'PAGO'),
# MAGIC   (102, 2, 'Mouse',    2, 80.00,   DATE'2026-09-02', 'PAGO'),
# MAGIC   (103, 3, 'Monitor',  1, 1200.00, DATE'2026-09-03', 'PENDENTE'),
# MAGIC   (104, 1, 'Teclado',  1, 250.00,  DATE'2026-09-05', 'PENDENTE'),
# MAGIC   (105, 4, 'Headset',  1, 300.00,  DATE'2026-09-06', 'CANCELADO');

# COMMAND ----------

# MAGIC %md
# MAGIC ## (SQL) SHOW SCHEMAS IN catalogo;
# MAGIC
# MAGIC Confirmando o que foi criado.

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW SCHEMAS IN workspace;
