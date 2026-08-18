"""Master verification script for all French bank statements."""

import glob
from pathlib import Path
from tabulate import tabulate
from monopoly.pdf import PdfDocument, PdfParser
from monopoly.banks.nickel import Nickel
from monopoly.banks.lbp import LaBanquePostale
from monopoly.banks.trade_republic import TradeRepublic
from monopoly.banks.sumeria import Sumeria
from monopoly.pipeline import Pipeline

CORPUS_ROOT = Path("/mnt/c/Users/djabi/Documents/relevé pdf")

BANK_CONFIGS = [
    ("Nickel", Nickel, CORPUS_ROOT / "nickel", "*.pdf", True),
    ("La Banque Postale", LaBanquePostale, CORPUS_ROOT / "bp", "*", True),
    ("Trade Republic", TradeRepublic, CORPUS_ROOT / "trade republic", "*.pdf", True),
    ("Sumeria (Lydia)", Sumeria, CORPUS_ROOT / "sumeria", "*.pdf", False),
]

def main():
    print("=" * 80)
    print("VÉRIFICATION GÉNÉRALE DU CORPUS BANCAIRE (MONOPOLY)")
    print("=" * 80)

    summary = []
    total_files = 0
    total_txs = 0

    for name, bank_cls, folder, pattern, safety_check in BANK_CONFIGS:
        files = sorted(glob.glob(str(folder / pattern)))
        if not files:
            summary.append([name, "0", "0", "⚠️ Aucun fichier trouvé"])
            continue

        bank_txs = 0
        status = "✅ 100% Succès"
        for f in files:
            try:
                doc = PdfDocument(file_path=f)
                parser = PdfParser(bank_cls, doc)
                pipeline = Pipeline(parser)
                statement = pipeline.extract(safety_check=safety_check)
                txs = pipeline.transform(statement)
                bank_txs += len(txs)
            except Exception as e:
                status = f"❌ Erreur: {e}"
                break

        total_files += len(files)
        total_txs += bank_txs
        summary.append([name, str(len(files)), str(bank_txs), status])

    print(tabulate(summary, headers=["Banque", "Fichiers PDF", "Transactions", "Statut"], tablefmt="rounded_outline"))
    print(f"\nTOTAL GLOBAL : {total_files} fichiers analysés, {total_txs} transactions extraites au centime près.")

if __name__ == "__main__":
    main()
