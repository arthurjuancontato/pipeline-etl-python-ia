# Publicação no GitHub

Destino preparado: **arthurjuancontato/pipeline-etl-python-ia**.

A criação do repositório e o envio ainda não foram realizados. O remoto `origin` aponta para esse destino; o remoto `projeto-original` preserva a referência ao repositório anterior. A branch de publicação é `main`.

1. No GitHub, crie um repositório vazio chamado `pipeline-etl-python-ia` na conta `arthurjuancontato`.
2. Não inicialize README, licença ou gitignore pelo GitHub: os arquivos já existem localmente.
3. Confira `git status` e `git remote -v` na pasta desta versão.
4. Envie com `git push -u origin main`.
5. Acompanhe a aba Actions. O workflow de testes será executado após o primeiro envio.

Descrição sugerida:

> Pipeline ETL de campanhas com validação de dados, interface Streamlit e relatório HTML offline. Criado por Arthur Juan com auxílio de IA.

Tópicos sugeridos: `python`, `etl`, `pandas`, `pydantic`, `streamlit`, `data-quality`, `data-analysis`.

O `.env`, ambientes virtuais, arquivos de saída temporários e logs estão ignorados. O `output.html` é um artefato de demonstração intencionalmente versionado. O `.gitattributes` o identifica como gerado para que o código Python represente melhor a linguagem do projeto.

O histórico Git foi preservado da cópia integral solicitada. Ele contém versões anteriores dos CSVs e do relatório original; ignorar arquivos ou substituir o HTML atual não remove esse histórico.
