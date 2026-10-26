# Pipeline ETL com Python — versão com IA

**Autor: Arthur Juan. Desenvolvido por Arthur Juan com auxílio de Inteligência Artificial.**

Evolução do projeto original de Arthur Juan para validar dados de campanhas, exportar CSVs e gerar relatórios exploratórios. Esta versão mantém os dados e o relatório original e melhora a organização, as validações e o uso pela linha de comando ou interface web.

## Melhorias desta versão

- Núcleo de processamento separado da interface, reutilizado pela CLI e pelo Streamlit.
- Validação em lote com Pydantic e conversão com `itertuples`, evitando uma Series por linha.
- Validação de datas reais, textos obrigatórios, valores finitos e contagens não negativas.
- Detecção de colunas ausentes, cabeçalhos duplicados, aliases conflitantes e arquivos sem registros.
- Erros estruturados por registro e campo, com download pela interface.
- CSV de saída somente quando todo o arquivo é válido, com gravação temporária e substituição após conclusão.
- Proteção contra sobrescrever o arquivo de entrada com a saída ou relatório.
- Relatório exploratório opcional em modo mínimo, para reduzir o custo de geração.
- Testes automatizados para validação, erros, exportação e CLI.

## Preparação

Ambiente utilizado: **Python 3.12**. Abra o terminal na pasta que contém este README.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

No Linux/macOS, ative com `source .venv/bin/activate`.

## Linha de comando

Validar o CSV padrão e exportar para `outputs/dados_validados.csv`:

```powershell
python main.py
```

Selecionar entrada e saída:

```powershell
python main.py --entrada data_2025.csv --saida outputs/dados_2025_validados.csv
```

Gerar também um relatório exploratório:

```powershell
python main.py --entrada data.csv --relatorio outputs/relatorio.html
```

O relatório é gerado após validar e exportar os dados. Caso sua geração falhe, o CSV já exportado permanece disponível. O comando retorna código 0 em caso de sucesso, 1 para falhas de processamento e 2 para argumentos inválidos. Na CLI, são exibidos os primeiros 20 erros; a interface permite baixar todos.

Os caminhos padrão são relativos à pasta do projeto. Caminhos informados pelo usuário são relativos ao diretório atual do terminal. Consulte `python main.py --help` para ver as opções.

## Interface web

```powershell
python -m streamlit run src/aplicacao.py
```

Abra o endereço apresentado no terminal, envie um CSV e clique em **Validar dados**. Se houver erros, consulte a tabela e baixe o diagnóstico. Se o arquivo inteiro for válido, baixe os dados validados. O número de registro corresponde à posição do dado após o cabeçalho, começando em 1; não representa a linha física de CSVs com campos multilinha.

## Formato do CSV

UTF-8 (com ou sem BOM), separado por vírgulas, com cabeçalho:

| Coluna | Regra |
| --- | --- |
| `Organizador` | Inteiro não negativo, obrigatório |
| `Ano_Mes` | Texto não vazio, obrigatório |
| `Dia_da_Semana` | Texto não vazio, obrigatório |
| `Tipo_Dia` | Texto não vazio, obrigatório |
| `Objetivo` | Texto não vazio, obrigatório |
| `Date` | Data válida, como `2025-01-31` |
| `AdSet_name` | Texto opcional |
| `Amount_spent` | Número finito entre 0 e 1.200; padrão 0 se ausente |
| `Link_clicks` | Inteiro não negativo ou vazio |
| `Impressions` | Inteiro não negativo; padrão 0 se ausente |
| `Conversions` | Inteiro não negativo ou vazio |
| `Segmentação` | Texto opcional; aceita também `Segmentacao` |
| `Tipo_de_Anúncio` | Texto não vazio; aceita também `Tipo_de_Anuncio` |
| `Fase` | Texto não vazio, obrigatório |

Espaços nas extremidades dos nomes de colunas e dos textos são removidos. Colunas extras são ignoradas na exportação. Células vazias tornam-se `None`: campos não opcionais não aceitam células vazias, mesmo quando possuem padrão para colunas ausentes. A saída usa os nomes internos `Segmentacao` e `Tipo_de_Anuncio`, datas ISO e UTF-8 com BOM.

## Configuração

Não há credenciais ou serviços externos obrigatórios. Opcionalmente, configure variáveis no processo:

```powershell
$env:ETL_INPUT = 'data.csv'
$env:ETL_OUTPUT = 'outputs/dados_validados.csv'
python main.py
```

Argumentos da CLI têm prioridade sobre essas variáveis. O `.env.example` documenta os nomes; o `.env` local está ignorado pelo Git e **não é carregado automaticamente**. Não armazene tokens ou senhas em arquivos públicos.

## Estrutura

```text
pipeline-etl-python/
├── src/
│   ├── __init__.py
│   ├── pipeline.py        # Leitura, validação e exportação
│   ├── validador.py       # Regras de dados
│   └── aplicacao.py       # Interface Streamlit
├── tests/test_pipeline.py
├── main.py               # Linha de comando
├── data.csv
├── data_2025.csv
├── output.html           # Relatório preservado do projeto original
├── outputs/              # Novas saídas, ignoradas pelo Git
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Verificação

```powershell
python -m unittest discover -s tests -v
```

Os dois arquivos fornecidos foram processados nesta versão: `data.csv` com 2.697 registros e `data_2025.csv` com 419 registros.

## Autoria e origem

Projeto de **Arthur Juan**, desenvolvido e aprimorado **com auxílio de IA**, a partir de uma cópia integral do seu projeto original. A versão original permanece na pasta `Pipeline ETL com Python`; esta versão está na pasta `Pipeline ETL com Python(IA)`.

A cópia preserva o histórico Git e o remoto original. As melhorias estão na branch local `melhorias-ia`; publique em um repositório próprio para manter as duas versões separadas.

## Limites e dados públicos

O pipeline processa o CSV em memória e não possui integração com banco de dados, agendamento ou processamento distribuído. Para arquivos que excedam a memória disponível, será necessário implementar processamento em blocos.

Os CSVs e o HTML herdados estão versionados. Relatórios podem conter amostras dos dados: publique somente informações autorizadas para divulgação e anonimize dados privados antes de compartilhar.
