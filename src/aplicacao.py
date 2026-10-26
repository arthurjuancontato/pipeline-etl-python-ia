"""Interface de Arthur Juan, desenvolvida com auxílio de IA."""
import sys
from pathlib import Path

# Permite executar pelo Streamlit a partir de qualquer diretório.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
import streamlit as st

from src.pipeline import ler_csv, validar_dados


def main():
    st.set_page_config(page_title="Pipeline ETL | Arthur Juan", layout="wide")
    st.title("Validador de campanhas")
    st.caption("Projeto de Arthur Juan, desenvolvido com auxílio de IA.")
    st.write("Envie um CSV UTF-8 separado por vírgulas para validar e exportar os dados.")
    enviado = st.file_uploader("Arquivo CSV", type=["csv"])
    if enviado is None:
        return
    try:
        df = ler_csv(enviado)
        st.dataframe(df.head(20), use_container_width=True)
        if st.button("Validar dados", type="primary"):
            with st.spinner("Validando registros..."):
                resultado = validar_dados(df)
            if resultado.erros:
                st.error(f"{len(resultado.erros)} erro(s) em {resultado.total} registros.")
                erros = pd.DataFrame(resultado.erros)
                st.dataframe(erros, use_container_width=True)
                st.download_button("Baixar erros", erros.to_csv(index=False).encode("utf-8-sig"),
                                   "erros_validacao.csv", "text/csv")
            else:
                st.success(f"{resultado.total} registros validados.")
                st.download_button("Baixar dados validados",
                                   resultado.dataframe().to_csv(index=False).encode("utf-8-sig"),
                                   "dados_validados.csv", "text/csv")
    except (ValueError, OSError, UnicodeError, pd.errors.ParserError) as exc:
        st.error(f"Não foi possível processar o CSV: {exc}")


if __name__ == "__main__":
    main()
