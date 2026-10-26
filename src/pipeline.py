"""Leitura, validação em lote e exportação, sem dependência da interface."""
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO

import pandas as pd
from pydantic import TypeAdapter, ValidationError

from src.validador import PlanilhaVendas

ADAPTADOR = TypeAdapter(list[PlanilhaVendas])
ALIASES = {"Segmentação": "Segmentacao", "Tipo_de_Anúncio": "Tipo_de_Anuncio"}


@dataclass
class ResultadoValidacao:
    registros: list[PlanilhaVendas]
    erros: list[dict]
    total: int

    def dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([item.model_dump(mode="json") for item in self.registros])


def ler_csv(origem: str | Path | BinaryIO) -> pd.DataFrame:
    # Lê o cabeçalho separadamente para detectar duplicatas antes do Pandas renomeá-las.
    import csv
    from io import StringIO

    if hasattr(origem, "read"):
        conteudo = origem.read()
        if isinstance(conteudo, bytes):
            conteudo = conteudo.decode("utf-8-sig")
    else:
        conteudo = Path(origem).read_text(encoding="utf-8-sig")
    cabecalho = next(csv.reader(StringIO(conteudo)), [])
    normalizados = [ALIASES.get(nome.strip(), nome.strip()) for nome in cabecalho]
    if len(normalizados) != len(set(normalizados)):
        raise ValueError("CSV contém colunas duplicadas ou aliases conflitantes.")
    return pd.read_csv(StringIO(conteudo))


def validar_dados(df: pd.DataFrame) -> ResultadoValidacao:
    df = df.copy(deep=False)
    colunas = [ALIASES.get(str(c).strip(), str(c).strip()) for c in df.columns]
    if len(colunas) != len(set(colunas)):
        raise ValueError("CSV contém colunas duplicadas ou aliases conflitantes.")
    df.columns = colunas
    obrigatorias = {nome for nome, campo in PlanilhaVendas.model_fields.items() if campo.is_required()}
    faltantes = sorted(obrigatorias - set(colunas))
    if faltantes:
        raise ValueError("Colunas obrigatórias ausentes: " + ", ".join(faltantes))
    if df.empty:
        raise ValueError("O CSV não contém registros.")
    # itertuples evita criar uma Series por linha e preserva melhor os tipos.
    dados = [dict(zip(colunas, (None if pd.isna(v) else v for v in linha)))
             for linha in df.itertuples(index=False, name=None)]
    try:
        registros = ADAPTADOR.validate_python(dados)
        return ResultadoValidacao(registros, [], len(df))
    except ValidationError as exc:
        erros = [{"registro": erro["loc"][0] + 1,
                  "campo": str(erro["loc"][1]), "mensagem": erro["msg"]}
                 for erro in exc.errors(include_input=False, include_url=False)]
        return ResultadoValidacao([], erros, len(df))


def exportar_csv(resultado: ResultadoValidacao, destino: str | Path) -> None:
    if resultado.erros or not resultado.registros:
        raise ValueError("Exportação exige um arquivo inteiramente válido.")
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    # Substituição somente após gravar o arquivo completo.
    import os
    import tempfile
    temporario = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8-sig", newline="",
                                         dir=destino.parent, suffix=".tmp", delete=False) as arquivo:
            temporario = Path(arquivo.name)
            resultado.dataframe().to_csv(arquivo, index=False)
        os.replace(temporario, destino)
    finally:
        if temporario is not None:
            temporario.unlink(missing_ok=True)
