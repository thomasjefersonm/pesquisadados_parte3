# Databricks notebook source
# MAGIC %md
# MAGIC # 004 - Data Quality: BRONZE → SILVER
# MAGIC
# MAGIC ## df = spark.read.format('delta').table("schema.tabela")
# MAGIC
# MAGIC Gera um dataframe para cada tabela delta da bronze.

# COMMAND ----------

df_clientes = spark.read.format("delta").table("bronze.clientes")
df_pedidos  = spark.read.format("delta").table("bronze.pedidos")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Aplicando Data Quality
# MAGIC
# MAGIC | Regra | O que faz |
# MAGIC |---|---|
# MAGIC | Nomenclatura | Colunas em maiúsculas e sem siglas (`ID_` → `CODIGO_`, `UF` → `UNIDADE_FEDERATIVA`) |
# MAGIC | Limpeza de texto | Remove espaços das pontas; nomes, cidades e produtos com iniciais maiúsculas; UF e status em maiúsculas |
# MAGIC | Tipagem | `DATA_PEDIDO` como `date` e `VALOR_UNITARIO` como `decimal(10,2)` |
# MAGIC | Duplicidade | Remove registros duplicados pela chave |
# MAGIC | Regras de negócio | Descarta quantidade e valor menores ou iguais a zero; calcula `VALOR_TOTAL` |
# MAGIC | Auditoria | Troca `DATA_HORA_BRONZE`/`NOME_ARQUIVO` por `NOME_ARQUIVO_BRONZE` e `DATA_ARQUIVO_SILVER` |

# COMMAND ----------

from pyspark.sql import functions as F

# ---------- Helpers ----------
def _apply_name_rules(colname: str) -> str:
    """Regras de renome: upper + prefixos 'ID_' e sufixo '_UF'."""
    n = colname.upper()
    n = n.replace("ID_", "CODIGO_")
    if n == "UF":
        n = "UNIDADE_FEDERATIVA"
    return n

def _safe_drop(df, cols):
    """Dropa colunas somente se existirem."""
    existing = set(df.columns)
    to_drop = [c for c in cols if c in existing]
    return df.drop(*to_drop) if to_drop else df

def _auditoria(df, src_fqn):
    """Remove as colunas de auditoria da bronze e adiciona as da silver."""
    df = _safe_drop(df, ["DATA_HORA_BRONZE", "NOME_ARQUIVO"])
    return (df
            .withColumn("NOME_ARQUIVO_BRONZE", F.lit(src_fqn))
            .withColumn("DATA_ARQUIVO_SILVER", F.current_timestamp()))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Clientes

# COMMAND ----------

df_clientes = df_clientes.toDF(*[_apply_name_rules(c) for c in df_clientes.columns])

df_clientes = (df_clientes
    .withColumn("NOME", F.initcap(F.trim("NOME")))
    .withColumn("CIDADE", F.initcap(F.trim("CIDADE")))
    .withColumn("UNIDADE_FEDERATIVA", F.upper(F.trim("UNIDADE_FEDERATIVA")))
    .dropDuplicates(["CODIGO_CLIENTE"]))

df_clientes = _auditoria(df_clientes, "bronze.clientes")

df_clientes.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("silver.clientes")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Pedidos

# COMMAND ----------

df_pedidos = df_pedidos.toDF(*[_apply_name_rules(c) for c in df_pedidos.columns])

df_pedidos = (df_pedidos
    .withColumn("PRODUTO", F.initcap(F.trim("PRODUTO")))
    .withColumn("STATUS", F.upper(F.trim("STATUS")))
    .withColumn("DATA_PEDIDO", F.to_date("DATA_PEDIDO"))
    .withColumn("VALOR_UNITARIO", F.col("VALOR_UNITARIO").cast("decimal(10,2)"))
    .filter((F.col("QUANTIDADE") > 0) & (F.col("VALOR_UNITARIO") > 0))
    .dropDuplicates(["CODIGO_PEDIDO"])
    .withColumn("VALOR_TOTAL", (F.col("QUANTIDADE") * F.col("VALOR_UNITARIO")).cast("decimal(12,2)")))

df_pedidos = _auditoria(df_pedidos, "bronze.pedidos")

df_pedidos.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("silver.pedidos")

# COMMAND ----------

# MAGIC %md
# MAGIC ## (SQL) SHOW TABLES IN silver
# MAGIC
# MAGIC Verifica os dados gravados no formato delta lake tipo MANAGED na camada silver.

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN silver

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM silver.clientes

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM silver.pedidos

# COMMAND ----------

# MAGIC %md
# MAGIC ## (SQL) DESCRIBE EXTENDED nome_tabela;
# MAGIC
# MAGIC Mostra se a tabela é MANAGED ou EXTERNAL.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED silver.pedidos;
