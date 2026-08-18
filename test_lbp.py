import glob
from monopoly.pdf import PdfDocument, PdfParser
from monopoly.banks.lbp import LaBanquePostale
from monopoly.pipeline import Pipeline

files = sorted(glob.glob('/mnt/c/Users/djabi/Documents/relevé pdf/bp/*'))
print(f"Test sur {len(files)} fichiers La Banque Postale :")

for f in files:
    doc = PdfDocument(file_path=f)
    parser = PdfParser(LaBanquePostale, doc)
    pipeline = Pipeline(parser)
    statement = pipeline.extract()
    transactions = pipeline.transform(statement)
    print(f"✅ {f.split('/')[-1]} : {len(transactions)} transactions (date relevé: {statement.statement_date.strftime('%Y-%m-%d')})")
