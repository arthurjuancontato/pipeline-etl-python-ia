# Pipeline ETL com Python · IA

**Autor: Arthur Juan — desenvolvido com auxílio de Inteligência Artificial.**

Validação e análise de campanhas publicitárias, da leitura do CSV à entrega de um relatório interativo. Uma evolução do [projeto original de Arthur Juan](https://github.com/arthurjuancontato/pipeline-etl-python), organizada para o repositório **pipeline-etl-python-ia**.

## O que você pode fazer

- Validar datas, campos obrigatórios, contagens e limites de investimento.
- Identificar erros por registro e campo, sem exportar uma base inválida.
- Explorar um exemplo ou enviar seu CSV pela interface Streamlit.
- Exportar dados validados e um relatório HTML que funciona offline.
- Filtrar os indicadores por mês, consultar qualidade, baixar o resumo e imprimir em PDF.

## Veja o relatório

Baixe e abra **[output.html](output.html)** no navegador. O GitHub exibe o código HTML; use **Download raw file** para abrir o relatório localmente.

O relatório traz investimento, impressões, conversões, distribuição mensal e valores ausentes. Não pressupõe uma moeda: os valores mantêm a unidade da fonte. Totais parciais recebem um asterisco e valores inteiramente ausentes aparecem como traço. O HTML contém somente agregados e contagens de qualidade, sem nomes de anúncios ou amostras individuais.

O visual usa fundo escuro e destaques em verde, adapta-se a telas menores e possui estilos próprios para impressão. Não depende de CDN, fontes externas ou conexão de rede.

## Começar

Use **Python 3.11 ou 3.12**. Na pasta do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run src/aplicacao.py
```

No Linux/macOS, substitua a ativação por `source .venv/bin/activate`.

Na interface, selecione **Explorar exemplo** ou envie um CSV. A validação ocorre automaticamente. As abas **Visão dos dados**, **Qualidade** e **Exportar** organizam os resultados. O processamento é armazenado em cache por conteúdo do arquivo, mantendo os downloads disponíveis nas novas interações.

## Executar pelo terminal

```powershell
# Valida data.csv e exporta para outputs/dados_validados.csv
python main.py

# Seleciona os caminhos e cria um relatório
python main.py --entrada data_2025.csv --saida outputs/dados_2025.csv --relatorio outputs/relatorio_2025.html

# Atualiza o relatório incluído no repositório
python main.py --relatorio output.html

# Executa os testes
python -m unittest discover -s tests -v
```

A CLI retorna **0** em sucesso, **1** em falhas de processamento e **2** em argumentos inválidos. Exibe até 20 erros; a interface disponibiliza o diagnóstico completo. Os caminhos padrão apontam para a pasta do projeto; caminhos informados são relativos ao diretório atual do terminal.

O CSV só é exportado quando todos os registros são válidos. A gravação usa arquivo temporário e substituição após conclusão. A entrada, a saída e o relatório devem ter destinos diferentes. O relatório é gerado após o CSV: caso falhe, o CSV já exportado permanece disponível.

## Contrato dos dados

CSV UTF-8, com ou sem BOM, separado por vírgulas. Cabeçalhos duplicados, aliases conflitantes, campos sem nome, aspas inválidas e linhas com quantidade incorreta de campos são rejeitados.

| Campo | Regra |
| --- | --- |
| `Organizador` | Inteiro não negativo obrigatório |
| `Ano_Mes`, `Dia_da_Semana`, `Tipo_Dia`, `Objetivo`, `Fase` | Textos obrigatórios não vazios |
| `Date` | Data válida, como `2025-01-31` |
| `Amount_spent` | Valor finito de 0 a 1.200; padrão 0 quando a coluna está ausente |
| `Impressions` | Inteiro não negativo; padrão 0 quando a coluna está ausente |
| `Link_clicks`, `Conversions` | Inteiros não negativos ou vazios |
| `AdSet_name` | Texto opcional |
| `Segmentação` ou `Segmentacao` | Texto opcional |
| `Tipo_de_Anúncio` ou `Tipo_de_Anuncio` | Texto obrigatório não vazio |

Espaços nas extremidades dos nomes e textos são removidos. Células vazias tornam-se `None`; campos não opcionais rejeitam essas células mesmo quando possuem padrão para colunas ausentes. Colunas extras são ignoradas na exportação. A saída usa os nomes internos sem acentos, datas ISO e UTF-8 com BOM.

Os números de registro no diagnóstico começam em 1 após o cabeçalho e não representam a linha física de CSVs com campos multilinha. Duplicatas são contadas no relatório, mas não removidas automaticamente.

## Organização

```text
pipeline-etl-python-ia/
├── .github/workflows/tests.yml  # Verificação automática no GitHub
├── .streamlit/config.toml       # Tema da interface
├── src/
│   ├── aplicacao.py             # Interface, cache e downloads
│   ├── pipeline.py              # Leitura, validação e exportação
│   ├── validador.py             # Modelo Pydantic
│   ├── relatorio.py             # Agregações e geração do HTML
│   └── relatorio.html           # Template visual e interações
├── tests/                      # Testes de processamento, relatório e interface
├── data.csv
├── data_2025.csv
├── main.py                     # CLI
├── output.html                 # Relatório pronto para abrir
├── requirements.txt            # Dependências diretas
├── requirements-lock.txt       # Ambiente validado para reprodução
└── PUBLICACAO.md               # Preparação do repositório no GitHub
```

## Configuração e dependências

Não são necessários tokens, serviços de IA ou credenciais para executar o projeto. “Com IA” descreve o auxílio no desenvolvimento, não uma integração com modelos durante a execução.

As dependências diretas são **Pandas**, **Pydantic** e **Streamlit**. A geração do relatório usa a biblioteca padrão e Pandas. Para reproduzir o ambiente validado, use `python -m pip install -r requirements-lock.txt` em Python 3.12.

Opcionalmente, configure `ETL_INPUT` e `ETL_OUTPUT` no ambiente do processo. Argumentos da CLI têm prioridade. O `.env.example` documenta esses nomes; o `.env` local é ignorado pelo Git e não é carregado automaticamente.

```powershell
$env:ETL_INPUT = 'data.csv'
$env:ETL_OUTPUT = 'outputs/dados_validados.csv'
```

## Qualidade e limites

Os testes cobrem validação, exportação segura, CSV malformado, dados ausentes, agregações, escape de HTML e persistência da interface. O workflow está preparado para executar os testes em Python 3.11 e 3.12 a cada push ou pull request.

O processamento usa memória e não é destinado a arquivos maiores que a memória disponível. Não há banco de dados, agendamento ou garantia de veracidade dos dados de origem. Na interface, arquivos enviados são processados no servidor que executa o Streamlit; ao hospedar a aplicação, considere esse servidor e seu cache no tratamento dos dados.

Os CSVs continuam versionados, assim como seu histórico herdado do original. Publique somente dados autorizados para divulgação. O novo relatório reduz a exposição de detalhes, mas seus totais agregados também devem ser apropriados para compartilhamento.

## Autoria

Criado por **Arthur Juan**, com auxílio de **Inteligência Artificial** nas melhorias de código, testes, documentação e apresentação. O projeto original e esta evolução são mantidos separadamente.
