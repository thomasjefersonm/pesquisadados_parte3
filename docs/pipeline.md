# Pipeline medalhão

| Camada | Local no Databricks | Formato | Notebook |
|---|---|---|---|
| Origem | schema `workspace.lojadb` | Tabelas relacionais | `001_preparando_ambiente` |
| LANDING/DADOS | `/Volumes/workspace/landing/dados` | CSV | `002_extracao_para_landing` |
| BRONZE | schema `workspace.bronze` | Delta (MANAGED) | `003_landing_para_bronze` |
| SILVER | schema `workspace.silver` | Delta (MANAGED) | `004_bronze_para_silver` |
| GOLD | schema `workspace.gold` | Delta (MANAGED) | `005_silver_para_gold` |

## 1. Extração → LANDING/DADOS
Lista todas as tabelas de `lojadb` (`SHOW TABLES`) e grava um CSV por tabela no volume.

![Landing](img/03_landing.png)

## 2. Ingestão → BRONZE
Um DataFrame por arquivo, com as colunas de metadado `data_hora_bronze` e `nome_arquivo`, gravado com `saveAsTable` (tabela MANAGED).

![Bronze](img/04_bronze.png)

## 3. Data Quality → SILVER

| Regra | O que faz |
|---|---|
| Nomenclatura | Colunas em maiúsculas e sem siglas (`ID_` → `CODIGO_`, `UF` → `UNIDADE_FEDERATIVA`) |
| Limpeza de texto | Remove espaços das pontas; nomes, cidades e produtos com iniciais maiúsculas; UF e status em maiúsculas |
| Tipagem | `DATA_PEDIDO` como `date` e `VALOR_UNITARIO` como `decimal(10,2)` |
| Duplicidade | Remove registros duplicados pela chave |
| Regras de negócio | Descarta quantidade e valor menores ou iguais a zero; calcula `VALOR_TOTAL` |
| Auditoria | `NOME_ARQUIVO_BRONZE` e `DATA_ARQUIVO_SILVER` |

![Silver](img/05_silver.png)

## 4. Modelagem dimensional → GOLD
Modelo estrela (Ralph Kimball): `fato_pedidos` ligada a `dim_cliente`, `dim_produto` e `dim_tempo`. As dimensões usam chave substituta (`SK_`, *identity*) e são carregadas com `MERGE` (SCD1).

```
             dim_cliente
                  │
dim_produto ── fato_pedidos ── dim_tempo
```

![Gold](img/06_gold.png)
