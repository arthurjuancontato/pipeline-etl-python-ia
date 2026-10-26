"""Aplicação de Arthur Juan, desenvolvida com auxílio de IA."""
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
import streamlit as st

from src.pipeline import ler_csv, validar_dados
from src.relatorio import gerar_html

RAIZ = Path(__file__).resolve().parents[1]


@st.cache_data(show_spinner=False)
def processar(conteudo: bytes):
    df = ler_csv(io.BytesIO(conteudo))
    return df, validar_dados(df)


def main():
    st.set_page_config(page_title="Data Lab | Arthur Juan", page_icon="📊", layout="wide")
    st.caption("ARTHUR JUAN / DATA LAB")
    st.title("Dados confiáveis. Decisões mais claras.")
    st.write("Valide campanhas, acompanhe a qualidade e exporte um relatório pronto para compartilhar.")
    with st.sidebar:
        st.header("Fonte dos dados")
        modo = st.radio("Escolha a entrada", ["Enviar CSV", "Explorar exemplo"])
        st.caption("CSV UTF-8, separado por vírgulas. O processamento usa a memória do servidor.")
        st.divider()
        st.caption("Autor: Arthur Juan. Desenvolvido com auxílio de IA.")
    if modo == "Explorar exemplo":
        conteudo = (RAIZ / 'data.csv').read_bytes()
    else:
        enviado = st.file_uploader("Selecione seu arquivo de campanhas", type=['csv'])
        if enviado is None:
            st.info("Envie um arquivo ou selecione Explorar exemplo na barra lateral.")
            return
        conteudo = enviado.getvalue()
    try:
        with st.spinner("Lendo e validando a base..."):
            df, resultado = processar(conteudo)
        col1, col2, col3 = st.columns(3)
        col1.metric("Registros", f"{len(df):,}".replace(',', '.'))
        col2.metric("Campos", len(df.columns))
        col3.metric("Erros de validação", len(resultado.erros))
        dados, qualidade, exportacao = st.tabs(["Visão dos dados", "Qualidade", "Exportar"])
        with dados:
            st.dataframe(df, width='stretch', hide_index=True)
        with qualidade:
            faltantes = df.isna().sum().rename('Células ausentes').to_frame()
            st.dataframe(faltantes, width='stretch')
            if resultado.erros:
                st.error("Corrija os campos indicados antes de exportar a base.")
                erros = pd.DataFrame(resultado.erros)
                st.dataframe(erros, width='stretch', hide_index=True)
                st.download_button("Baixar diagnóstico CSV", erros.to_csv(index=False).encode('utf-8-sig'),
                                   'erros_validacao.csv', 'text/csv')
            else:
                st.success("Todos os registros passaram pelas regras de validação.")
            st.caption("Campos opcionais vazios são permitidos. Validação não garante a exatidão dos dados de origem.")
        with exportacao:
            if resultado.erros:
                st.warning("Exportação indisponível enquanto houver erros.")
            else:
                validado = resultado.dataframe()
                st.subheader("Pronto para o próximo passo")
                st.download_button("Baixar CSV validado", validado.to_csv(index=False).encode('utf-8-sig'),
                                   'dados_validados.csv', 'text/csv', type='primary')
                st.download_button("Baixar relatório HTML", gerar_html(validado).encode('utf-8'),
                                   'relatorio_campanhas.html', 'text/html')
                st.caption("O relatório funciona offline e inclui somente agregados mensais e contagens de qualidade.")
    except (ValueError, OSError, UnicodeError) as exc:
        st.error(f"Não foi possível processar o arquivo: {exc}")


if __name__ == '__main__':
    main()
