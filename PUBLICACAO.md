# Manutenção e publicação

Repositório: [arthurjuancontato/pipeline-etl-python-ia](https://github.com/arthurjuancontato/pipeline-etl-python-ia).

A branch principal é `main`. Para publicar atualizações após revisar e testar:

```powershell
python -m unittest discover -s tests -v
git status
git add <arquivos-revisados>
git commit -m "Descreve a atualização"
git push origin main
```

O workflow da aba Actions executa os testes após push ou pull request. O remoto `projeto-original` é uma referência à origem histórica; atualizações desta versão devem ser enviadas somente ao `origin` terminado em `-ia.git`.

O `.env`, ambientes virtuais, caches, saídas temporárias e logs estão ignorados. O `output.html` é uma demonstração intencionalmente versionada. Atualize-o com `python main.py --relatorio output.html` quando os dados ou o template mudarem.

O histórico Git foi preservado da cópia integral solicitada. Ele contém versões anteriores dos CSVs e do relatório original. Antes de adicionar outros dados, verifique se podem ser divulgados publicamente.
