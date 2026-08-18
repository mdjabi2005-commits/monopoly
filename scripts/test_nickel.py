import glob
from monopoly.pdf import PdfDocument, PdfParser
from monopoly.banks.nickel import Nickel
from monopoly.pipeline import Pipeline

files = sorted(glob.glob('/mnt/c/Users/djabi/Documents/relevé pdf/nickel/*.pdf'))
print(f"Test sur {len(files)} fichiers Nickel :")

for f in files:
    doc = PdfDocument(file_path=f)
    parser = PdfParser(Nickel, doc)
    pipeline = Pipeline(parser)
    statement = pipeline.extract()
    transactions = pipeline.transform(statement)
    print(f"✅ {f.split('/')[-1]} : {len(transactions)} transactions (date relevé: {statement.statement_date.strftime('%Y-%m-%d')})")
