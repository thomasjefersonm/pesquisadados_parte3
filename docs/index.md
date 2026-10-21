# Contextualização

Trabalho 3 de Engenharia de Dados (SATC): pipeline de dados no **Databricks Free Edition** com a **arquitetura medalhão** (Landing → Bronze → Silver → Gold), orquestrado por um Job em **Jobs & Pipelines**.

É a continuação dos trabalhos [1](https://github.com/thomasjefersonm/pesquisadados) e [2](https://github.com/thomasjefersonm/pesquisadados_parte2): os mesmos dados (`clientes` e `pedidos` do banco `LojaDB`), agora todos dentro do Databricks.

```
lojadb (origem) → LANDING/DADOS (CSV) → BRONZE (Delta) → SILVER (Delta) → GOLD (Kimball)
                  Notebook 002          Notebook 003     Notebook 004     Notebook 005
```

## Integrantes
- Thomas Jeferson da Silva Maggi
- Bruno Ghisi da Silva

## Banco de origem `lojadb`

| Tabela | Colunas |
|---|---|
| clientes | id_cliente, nome, cidade, uf |
| pedidos | id_pedido, id_cliente, produto, quantidade, valor_unitario, data_pedido, status |

![Preparando ambiente](img/02_preparando_ambiente.png)
