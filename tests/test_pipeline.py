import io
from pathlib import Path
import tempfile
import unittest

import pandas as pd

from main import main
from src.pipeline import exportar_csv, ler_csv, validar_dados


def registro(**alteracoes):
    item = dict(Organizador=1, Ano_Mes="2025 | Janeiro", Dia_da_Semana="Quarta-Feira",
                Tipo_Dia="Dia útil", Objetivo="Leads", Date="2025-01-01",
                Amount_spent=10, Impressions=20, Tipo_de_Anúncio="Video", Fase="Leads")
    return item | alteracoes


class PipelineTest(unittest.TestCase):
    def test_valido_aliases_opcionais_e_exportacao(self):
        resultado = validar_dados(pd.DataFrame([registro()]))
        self.assertFalse(resultado.erros)
        self.assertIsNone(resultado.registros[0].Segmentacao)
        with tempfile.TemporaryDirectory() as pasta:
            destino = Path(pasta) / "sub" / "saida.csv"
            exportar_csv(resultado, destino)
            self.assertEqual(pd.read_csv(destino).loc[0, "Date"], "2025-01-01")

    def test_multiplos_erros_em_lote(self):
        resultado = validar_dados(pd.DataFrame([
            registro(Date="2025-02-30", Amount_spent=1201),
            registro(Impressions=-1, Link_clicks=-2),
        ]))
        self.assertEqual(len(resultado.erros), 4)
        self.assertEqual({e['registro'] for e in resultado.erros}, {1, 2})
        self.assertFalse(resultado.registros)

    def test_colunas_ausentes_e_csv_vazio(self):
        with self.assertRaisesRegex(ValueError, "obrigatórias"):
            validar_dados(pd.DataFrame([{"Organizador": 1}]))
        with self.assertRaisesRegex(ValueError, "não contém registros"):
            validar_dados(pd.DataFrame([registro()]).iloc[:0])

    def test_colunas_duplicadas_e_aliases_conflitantes(self):
        for texto in ["Date,Date\n2025-01-01,2025-01-01", "Segmentação,Segmentacao\na,b"]:
            with self.assertRaisesRegex(ValueError, "duplicadas"):
                ler_csv(io.BytesIO(texto.encode("utf-8")))

    def test_ausentes_e_infinito(self):
        resultado = validar_dados(pd.DataFrame([registro(Link_clicks=float('nan'), Amount_spent=float('inf'))]))
        self.assertEqual(resultado.erros[0]['campo'], 'Amount_spent')
        resultado = validar_dados(pd.DataFrame([registro(Link_clicks=float('nan'))]))
        self.assertIsNone(resultado.registros[0].Link_clicks)

    def test_entrada_nao_e_modificada(self):
        df = pd.DataFrame([registro()])
        original = df.copy(deep=True)
        validar_dados(df)
        pd.testing.assert_frame_equal(df, original)

    def test_exportacao_invalida_preserva_saida(self):
        resultado = validar_dados(pd.DataFrame([registro(Impressions=-1)]))
        with tempfile.TemporaryDirectory() as pasta:
            destino = Path(pasta) / "saida.csv"
            destino.write_text("preservar", encoding="utf-8")
            with self.assertRaises(ValueError):
                exportar_csv(resultado, destino)
            self.assertEqual(destino.read_text(encoding="utf-8"), "preservar")

    def test_cli_exporta_e_recusa_sobrescrever_entrada(self):
        with tempfile.TemporaryDirectory() as pasta:
            entrada, saida = Path(pasta) / 'entrada.csv', Path(pasta) / 'saida.csv'
            pd.DataFrame([registro()]).to_csv(entrada, index=False)
            self.assertEqual(main(['--entrada', str(entrada), '--saida', str(saida)]), 0)
            self.assertTrue(saida.exists())
            with self.assertRaises(SystemExit):
                main(['--entrada', str(entrada), '--saida', str(entrada)])


if __name__ == '__main__':
    unittest.main()
