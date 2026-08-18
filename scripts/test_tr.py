import glob
from monopoly.pdf import PdfDocument, PdfParser
from monopoly.banks.trade_republic import TradeRepublic
from monopoly.pipeline import Pipeline
from tabulate import tabulate

files = sorted(glob.glob('/mnt/c/Users/djabi/Documents/relevé pdf/trade republic/*.pdf'))
print(f"Test sur {len(files)} fichiers Trade Republic :")

total_txs = 0
for f in files:
    doc = PdfDocument(file_path=f)
    parser = PdfParser(TradeRepublic, doc)
    pipeline = Pipeline(parser)
    statement = pipeline.extract()
    transactions = pipeline.transform(statement)
    total_txs += len(transactions)
    print(f"✅ {f.split('/')[-1]} : {len(transactions)} transactions (période au: {statement.statement_date.strftime('%Y-%m-%d')})")

print(f"\nTOTAL TRADE REPUBLIC : {total_txs} transactions extraites avec succès sur {len(files)}/{len(files)} fichiers !")
