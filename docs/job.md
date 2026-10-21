# 5. Jobs & Pipelines

## O que é um Job
**Jobs & Pipelines** é o orquestrador do Databricks. Um **Job** reúne várias **tarefas** (aqui, notebooks) e define a ordem e as dependências entre elas. Assim o pipeline inteiro roda com um clique, ou por agendamento, sem executar notebook por notebook, e uma etapa só começa se a anterior terminar com sucesso.

## O Job `job_lakehouse_medalhao`
Cada tarefa depende da anterior (`depends_on`), formando a sequência da arquitetura medalhão:

```
001_preparando_ambiente → 002_extracao_para_landing → 003_landing_para_bronze → 004_bronze_para_silver → 005_silver_para_gold
```

| Tarefa | Notebook | Etapa |
|---|---|---|
| 1 | `001_preparando_ambiente` | Schemas, volume e banco de origem |
| 2 | `002_extracao_para_landing` | Extração → LANDING/DADOS (CSV) |
| 3 | `003_landing_para_bronze` | Ingestão → BRONZE (Delta) |
| 4 | `004_bronze_para_silver` | Data Quality → SILVER |
| 5 | `005_silver_para_gold` | Modelagem dimensional → GOLD |

Todas as tarefas usam computação **serverless**. A definição do Job está em `resources/job_medalhao.json` e pode ser recriada em *Jobs & Pipelines → Create job → Edit as JSON*. O notebook `006_destruindo_ambiente` fica fora do Job, pois só serve para limpar o ambiente.

![Job](img/07_job.jpg)

## Execução
Execução completa com sucesso: as 5 tarefas em sequência, em cerca de 3 minutos.

| Tarefa | Status | Duração |
|---|---|---|
| 001_preparando_ambiente | Succeeded | 1m 5s |
| 002_extracao_para_landing | Succeeded | 16s |
| 003_landing_para_bronze | Succeeded | 27s |
| 004_bronze_para_silver | Succeeded | 26s |
| 005_silver_para_gold | Succeeded | 45s |

![Execução do Job](img/08_job_execucao.jpg)

## Resultado no catálogo
Depois da execução, o catálogo `workspace` contém os schemas `lojadb`, `landing`, `bronze`, `silver` e `gold`:

![Catálogo](img/09_catalogo.jpg)
