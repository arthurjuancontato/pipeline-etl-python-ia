import io
from pathlib import Path
import json
import re
import unittest
import pandas as pd
from src.pipeline import ler_csv, validar_dados
from src.relatorio import gerar_html, resumo
from test_pipeline import registro


class RelatorioTest(unittest.TestCase):
    def test_agregados_e_ausencia_nao_zero(self):
        df = validar_dados(pd.DataFrame([registro(), registro(Amount_spent=20)])).dataframe()
        dados = resumo(df)
        self.assertEqual(dados['meses'][0]['investimento'], 30)
        self.assertIsNone(dados['meses'][0]['conversoes'])
        self.assertEqual(dados['meses'][0]['conversoes_ausentes'], 2)

    def test_relatorio_sem_linhas_individuais_e_json_seguro(self):
        df = validar_dados(pd.DataFrame([registro(AdSet_name='SEGREDO_DE_TESTE')])).dataframe()
        df['</script><script>alert(1)</script>'] = None
        html = gerar_html(df)
        self.assertNotIn('SEGREDO_DE_TESTE', html)
        self.assertNotIn('</script><script>alert(1)', html)
        payload = re.search(r'type="application/json">(.*?)</script>', html).group(1)
        self.assertEqual(json.loads(payload)['registros'], 1)

    def test_csv_malformado(self):
        for texto in ['a,b\n1,2,3', 'a,b\n1', 'a,\n1,2', 'a,b\n"ab,2', '']:
            with self.assertRaises(ValueError):
                ler_csv(io.BytesIO(texto.encode()))

    def test_interface_exemplo_e_downloads_persistem(self):
        from streamlit.testing.v1 import AppTest
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'src' / 'aplicacao.py')).run()
        self.assertFalse(app.exception)
        app.radio[0].set_value('Explorar exemplo').run()
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[0].value, '2.697')
        app.run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.get('download_button')), 2)
