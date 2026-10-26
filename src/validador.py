"""Modelo de campanhas. Autor: Arthur Juan, com auxílio de IA."""
from datetime import date
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

Texto = Annotated[str, Field(min_length=1)]
Contagem = Annotated[int, Field(ge=0)]


class PlanilhaVendas(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, allow_inf_nan=False)

    Organizador: Contagem
    Ano_Mes: Texto
    Dia_da_Semana: Texto
    Tipo_Dia: Texto
    Objetivo: Texto
    Date: date
    AdSet_name: str | None = None
    Amount_spent: float = Field(default=0.0, ge=0, le=1200)
    Link_clicks: Contagem | None = None
    Impressions: Contagem = 0
    Conversions: Contagem | None = None
    Segmentacao: str | None = None
    Tipo_de_Anuncio: Texto
    Fase: Texto
