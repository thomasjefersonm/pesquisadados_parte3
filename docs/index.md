# Contextualização do Trabalho

Trabalho 3 da disciplina **Engenharia de Dados** (Engenharia de Software – 5ª fase – SATC), professor Jorge Luiz da Silva.
É um **complemento dos trabalhos 1 e 2** ([trabalho 1](https://thomasjefersonm.github.io/pesquisadados/) e [trabalho 2](https://thomasjefersonm.github.io/pesquisadados_parte2/)), em repositório separado.

## Objetivo
Construir um pipeline de dados no **Databricks Free Edition** implementando a **arquitetura medalhão** (experiência PaaS): **Landing → Bronze → Silver → Gold**, com todas as etapas encadeadas em um Job de **Jobs & Pipelines**.

## Cenário e conjunto de dados
Mesma loja virtual fictícia dos trabalhos 1 e 2. O banco relacional de origem `LojaDB` é criado no próprio Databricks, no schema `workspace.lojadb`, pelo notebook `001_preparando_ambiente`:

| Tabela | Conteúdo |
|---|---|
| `clientes` | 4 clientes |
| `pedidos` | 5 pedidos |

### Modelo ER
![Modelo ER](assets/modelo_er.svg)

Um cliente possui vários pedidos (relação 1:N por `id_cliente`).

### DDL (Databricks SQL)
```sql
CREATE TABLE workspace.lojadb.clientes (
  id_cliente INT NOT NULL,
  nome       VARCHAR(100) NOT NULL,
  cidade     VARCHAR(100),
  uf         CHAR(2)
);

CREATE TABLE workspace.lojadb.pedidos (
  id_pedido      INT NOT NULL,
  id_cliente     INT NOT NULL,
  produto        VARCHAR(100) NOT NULL,
  quantidade     INT NOT NULL,
  valor_unitario DECIMAL(10,2) NOT NULL,
  data_pedido    DATE NOT NULL,
  status         VARCHAR(20) NOT NULL
);
```

## Arquitetura
```
lojadb (origem) ──▶ LANDING/DADOS (CSV) ──▶ BRONZE (Delta) ──▶ SILVER (Delta) ──▶ GOLD (Kimball)
```

## Notebooks
Executados em ordem, na pasta `notebooks/`: `001_preparando_ambiente`, `002_extracao_para_landing`, `003_landing_para_bronze`, `004_bronze_para_silver` e `005_silver_para_gold`. O `006_destruindo_ambiente` limpa o ambiente e não faz parte do Job.

## Integrantes
- Thomas Jeferson da Silva Maggi
- Bruno Ghisi da Silva
