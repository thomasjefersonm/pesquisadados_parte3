# pesquisadados_parte3

Trabalho 3 – **Lakehouse com Databricks Free Edition e Arquitetura Medalhão**
Engenharia de Dados · Engenharia de Software 5ª fase · SATC · Prof. Jorge Luiz da Silva

> 📚 Documentação completa (MkDocs): https://thomasjefersonm.github.io/pesquisadados_parte3/
>
> Complemento do [trabalho 1](https://github.com/thomasjefersonm/pesquisadados) e do [trabalho 2](https://github.com/thomasjefersonm/pesquisadados_parte2) (repositórios separados).

## Integrantes
- Thomas Jeferson da Silva Maggi
- Bruno Ghisi da Silva

## Arquitetura

```
┌──────────┐   ┌───────────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  lojadb  │──▶│ LANDING/DADOS │──▶│  BRONZE  │──▶│  SILVER  │──▶│   GOLD   │
│ (origem) │   │     (CSV)     │   │ (Delta)  │   │ (Delta)  │   │ (Kimball)│
└──────────┘   └───────────────┘   └──────────┘   └──────────┘   └──────────┘
                  Notebook 002      Notebook 003   Notebook 004   Notebook 005
       └────────── Job (Jobs & Pipelines): 001 → 002 → 003 → 004 → 005 ──────────┘
```

| # | Etapa | Notebook | Origem → Destino | Formato |
|---|---|---|---|---|
| 1 | Extração | `002_extracao_para_landing` | banco `lojadb` → schema **LANDING** / volume **DADOS** | CSV |
| 2 | Ingestão | `003_landing_para_bronze` | LANDING/DADOS → schema **BRONZE** | Delta Lake |
| 3 | Data Quality | `004_bronze_para_silver` | BRONZE → schema **SILVER** | Delta Lake |
| 4 | Modelagem | `005_silver_para_gold` | SILVER → schema **GOLD** (Ralph Kimball) | Delta Lake |
| 5 | Automação | Job `job_lakehouse_medalhao` | executa os notebooks em sequência | Jobs & Pipelines |

O notebook `001_preparando_ambiente` cria o banco relacional de origem `lojadb` (tabelas `clientes` e `pedidos`, as mesmas dos trabalhos 1 e 2), os schemas `landing`, `bronze`, `silver`, `gold` e o volume `landing.dados`. O `006_destruindo_ambiente` apaga tudo e não faz parte do Job.

## Ferramentas utilizadas

| Ferramenta | Para que serve |
|---|---|
| Databricks Free Edition | Plataforma PaaS (notebooks, Unity Catalog, Jobs & Pipelines) |
| Unity Catalog (catálogo `workspace`) | Schemas `lojadb`, `landing`, `bronze`, `silver`, `gold` e volume `landing.dados` |
| Apache Spark (PySpark / SQL) | Processamento dos dados |
| Delta Lake | Formato das tabelas gerenciadas (MANAGED) das camadas bronze, silver e gold |
| Git e GitHub | Versionamento (Git folder no Databricks) |
| MkDocs | Documentação publicada no GitHub Pages |

## Passo a passo

### 1. Importar o repositório no Databricks
*Workspace → Create → Git folder*, com a URL `https://github.com/thomasjefersonm/pesquisadados_parte3.git`.

![Git folder](docs/img/01_git_folder.png)

### 2. Preparando o ambiente (`001_preparando_ambiente`)

![Preparando ambiente](docs/img/02_preparando_ambiente.png)

### 3. Extração → LANDING/DADOS (`002_extracao_para_landing`)
Lista todas as tabelas do `lojadb` e grava um CSV por tabela em `/Volumes/workspace/landing/dados`.

![Landing](docs/img/03_landing.png)

### 4. Ingestão → BRONZE (`003_landing_para_bronze`)
Lê os CSVs e grava tabelas Delta MANAGED no schema `bronze`, com as colunas `data_hora_bronze` e `nome_arquivo`.

![Bronze](docs/img/04_bronze.png)

### 5. Data Quality → SILVER (`004_bronze_para_silver`)

| Regra | O que faz |
|---|---|
| Nomenclatura | Colunas em maiúsculas e sem siglas (`ID_` → `CODIGO_`, `UF` → `UNIDADE_FEDERATIVA`) |
| Limpeza de texto | Remove espaços das pontas; nomes, cidades e produtos com iniciais maiúsculas; UF e status em maiúsculas |
| Tipagem | `DATA_PEDIDO` como `date` e `VALOR_UNITARIO` como `decimal(10,2)` |
| Duplicidade | Remove registros duplicados pela chave |
| Regras de negócio | Descarta quantidade e valor menores ou iguais a zero; calcula `VALOR_TOTAL` |
| Auditoria | `NOME_ARQUIVO_BRONZE` e `DATA_ARQUIVO_SILVER` |

![Silver](docs/img/05_silver.png)

### 6. Modelagem dimensional → GOLD (`005_silver_para_gold`)
Modelo estrela (Ralph Kimball), com chaves substitutas (`SK_`) e carga por `MERGE` (SCD1):

```
             dim_cliente
                  │
dim_produto ── fato_pedidos ── dim_tempo
```

![Gold](docs/img/06_gold.png)

### 7. Jobs & Pipelines
Job `job_lakehouse_medalhao` com as tarefas `001 → 002 → 003 → 004 → 005`, cada uma dependente da anterior. Definição em [`resources/job_medalhao.json`](resources/job_medalhao.json) (*Jobs & Pipelines → Create job → Edit as JSON*).

![Job](docs/img/07_job.png)

![Execução do Job](docs/img/08_job_execucao.png)

### 8. Catálogo

![Catálogo](docs/img/09_catalogo.png)

## Documentação (MkDocs)
```bash
mkdocs serve       # visualizar em http://127.0.0.1:8000
mkdocs gh-deploy   # publicar no GitHub Pages
```

## Estrutura
```
pesquisadados_parte3/
├── README.md
├── mkdocs.yml
├── notebooks/
│   ├── 001_preparando_ambiente.py
│   ├── 002_extracao_para_landing.py
│   ├── 003_landing_para_bronze.py
│   ├── 004_bronze_para_silver.py
│   ├── 005_silver_para_gold.py
│   └── 006_destruindo_ambiente.py
├── resources/
│   └── job_medalhao.json     # definição do Job (Jobs & Pipelines)
└── docs/                     # páginas do MkDocs e prints (docs/img)
```

## Referências
- https://github.com/jlsilva01/databricks-free-edition (repositório modelo do professor)
- https://docs.databricks.com/
- https://www.databricks.com/glossary/medallion-architecture
- https://docs.databricks.com/workflows/jobs/index.html
- https://docs.databricks.com/data-governance/unity-catalog/index.html
- https://docs.delta.io/
- https://www.mkdocs.org
