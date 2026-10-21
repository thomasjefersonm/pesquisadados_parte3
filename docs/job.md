# Jobs & Pipelines

O Job `job_lakehouse_medalhao` executa os notebooks em sequência, cada tarefa dependente da anterior:

```
001_preparando_ambiente → 002_extracao_para_landing → 003_landing_para_bronze → 004_bronze_para_silver → 005_silver_para_gold
```

A definição está em `resources/job_medalhao.json` (fonte: este repositório no GitHub, branch `main`). O notebook `006_destruindo_ambiente` limpa o ambiente e não faz parte do Job.

![Job](img/07_job.png)

![Execução do Job](img/08_job_execucao.png)

![Catálogo](img/09_catalogo.png)
