import glob
from monopoly.pdf import PdfDocument, PdfParser
from monopoly.banks.lbp import LaBanquePostale
from monopoly.banks.nickel import Nickel
from monopoly.banks.trade_republic import TradeRepublic
from monopoly.pipeline import Pipeline
from tabulate import tabulate

print("=" * 80)
print("1. NICKEL - Relevé de juillet 2026")
print("=" * 80)
nickel_file = sorted(glob.glob('/mnt/c/Users/djabi/Documents/relevé pdf/nickel/*.pdf'))[-1]
doc = PdfDocument(file_path=nickel_file)
parser = PdfParser(Nickel, doc)
pipeline = Pipeline(parser)
statement = pipeline.extract()
txs = pipeline.transform(statement)

table = [[t.date, f"{t.amount:+.2f} €", t.description] for t in txs]
print(tabulate(table, headers=["Date", "Montant", "Description"], tablefmt="rounded_outline"))

print("\n" + "=" * 80)
print("2. LA BANQUE POSTALE - Relevé de juillet 2026")
print("=" * 80)
lbp_file = sorted(glob.glob('/mnt/c/Users/djabi/Documents/relevé pdf/bp/*'))[-1]
doc = PdfDocument(file_path=lbp_file)
parser = PdfParser(LaBanquePostale, doc)
pipeline = Pipeline(parser)
statement = pipeline.extract()
txs = pipeline.transform(statement)

table = [[t.date, f"{t.amount:+.2f} €", t.description] for t in txs]
print(tabulate(table, headers=["Date", "Montant", "Description"], tablefmt="rounded_outline"))

print("\n" + "=" * 80)
print("3. TRADE REPUBLIC - Relevé d'espèces (premières transactions)")
print("=" * 80)
tr_file = sorted(glob.glob('/mnt/c/Users/djabi/Documents/relevé pdf/trade republic/*.pdf'))[0]
doc = PdfDocument(file_path=tr_file)
parser = PdfParser(TradeRepublic, doc)
pipeline = Pipeline(parser)
statement = pipeline.extract()
txs = pipeline.transform(statement)

table = [[t.date, f"{t.amount:+.2f} €", f"{t.balance:.2f} €", t.description[:50]] for t in txs[:10]]
print(tabulate(table, headers=["Date", "Montant", "Solde", "Description"], tablefmt="rounded_outline"))
