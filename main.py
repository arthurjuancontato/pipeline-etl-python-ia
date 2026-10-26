"""CLI do pipeline de Arthur Juan, com auxílio de IA."""
import argparse
import os
from pathlib import Path
import sys

from src.pipeline import exportar_csv, ler_csv, validar_dados

RAIZ = Path(__file__).resolve().parent


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entrada", type=Path, default=Path(os.getenv("ETL_INPUT", str(RAIZ / "data.csv"))))
    parser.add_argument("--saida", type=Path, default=Path(os.getenv("ETL_OUTPUT", str(RAIZ / "outputs" / "dados_validados.csv"))))
    parser.add_argument("--relatorio", type=Path, help="Gera também relatório HTML após validar")
    args = parser.parse_args(argv)
    destinos = [args.saida] + ([args.relatorio] if args.relatorio else [])
    if len({p.resolve() for p in [args.entrada, *destinos]}) != 1 + len(destinos):
        parser.error("Entrada, saída e relatório devem ter caminhos diferentes.")
    try:
        resultado = validar_dados(ler_csv(args.entrada))
        if resultado.erros:
            print(f"Validação falhou: {len(resultado.erros)} erro(s).", file=sys.stderr)
            for erro in resultado.erros[:20]:
                print(f"Registro {erro['registro']}, {erro['campo']}: {erro['mensagem']}", file=sys.stderr)
            return 1
        exportar_csv(resultado, args.saida)
        print(f"{resultado.total} registros exportados para {args.saida}")
        if args.relatorio:
            from ydata_profiling import ProfileReport
            args.relatorio.parent.mkdir(parents=True, exist_ok=True)
            ProfileReport(resultado.dataframe(), title="Campanhas | Arthur Juan", minimal=True).to_file(args.relatorio)
            print(f"Relatório: {args.relatorio}")
        return 0
    except (ValueError, OSError, UnicodeError, ImportError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
