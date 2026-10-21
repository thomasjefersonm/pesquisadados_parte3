# 1. Extração → LANDING/DADOS

Notebook: `002_extracao_para_landing`

## O que é a camada landing
A **landing** é a "zona de pouso": recebe a **cópia bruta** dos dados exatamente como saíram da origem, em arquivos. Ela isola o banco de origem do restante do pipeline: depois da extração, nenhuma camada precisa consultar o banco novamente.

Como a origem é um banco **relacional**, o formato exigido é **CSV** (para um banco não relacional seria JSON).

## Como funciona
1. Lista **todas** as tabelas do banco de origem com `SHOW TABLES`. Como a lista vem do próprio banco, uma tabela nova também seria extraída sem mudar o código.
2. Lê cada tabela e grava um arquivo `<tabela>.csv`, com cabeçalho, no volume `dados` do schema `landing`.

```python
caminho_landing = '/Volumes/workspace/landing/dados'

tabelas = [t.tableName for t in spark.sql("SHOW TABLES IN workspace.lojadb").collect()]

for tabela in tabelas:
    df = spark.read.table(f"workspace.lojadb.{tabela}")
    df.toPandas().to_csv(f"{caminho_landing}/{tabela}.csv", index=False)
```

## Resultado

| Arquivo | Linhas | Tamanho |
|---|---|---|
| `/Volumes/workspace/landing/dados/clientes.csv` | 4 | 136 B |
| `/Volumes/workspace/landing/dados/pedidos.csv` | 5 | 282 B |

![Landing](img/03_landing.jpg)
