"""Relatório portátil: agregados reais, sem CDN ou amostras individuais."""
import json
from pathlib import Path

import pandas as pd


def resumo(df: pd.DataFrame) -> dict:
    dados = df.copy()
    dados['mes'] = pd.to_datetime(dados['Date']).dt.strftime('%Y-%m')
    meses = []
    for mes, grupo in dados.groupby('mes', sort=True):
        meses.append(dict(mes=mes, registros=len(grupo), investimento=float(grupo.Amount_spent.sum()),
                          impressoes=int(grupo.Impressions.sum()),
                          cliques=None if grupo.Link_clicks.notna().sum() == 0 else int(grupo.Link_clicks.sum()),
                          conversoes=None if grupo.Conversions.notna().sum() == 0 else int(grupo.Conversions.sum()),
                          cliques_ausentes=int(grupo.Link_clicks.isna().sum()),
                          conversoes_ausentes=int(grupo.Conversions.isna().sum())))
    ausentes = {coluna: int(total) for coluna, total in df.isna().sum().items() if total}
    return dict(meses=meses, ausentes=ausentes, registros=len(df), colunas=len(df.columns),
                duplicados=int(df.duplicated().sum()), inicio=str(dados.Date.min()), fim=str(dados.Date.max()))


def gerar_html(df: pd.DataFrame) -> str:
    # Evita fechamento de script e injeção de HTML por conteúdo dos dados.
    payload = json.dumps(resumo(df), ensure_ascii=False, allow_nan=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    template = Path(__file__).with_name('relatorio.html').read_text(encoding='utf-8-sig')
    return template.replace('__DADOS_JSON__', payload)
