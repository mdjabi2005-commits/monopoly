"""Quick validation script for Sumeria parser."""

from pathlib import Path

from monopoly.banks import Sumeria
from monopoly.pdf import PdfDocument, PdfParser
from monopoly.pipeline import Pipeline
from monopoly.statements import DebitStatement

pdf_path = Path(r"/mnt/c/Users/djabi/Documents/relevé pdf/sumeria/bank_statement_19246015.pdf")
document = PdfDocument(pdf_path)
parser = PdfParser(Sumeria, document)
pipeline = Pipeline(parser)
statement = pipeline.extract(safety_check=False)

print("bank:", parser.bank.name)
print("type:", statement.statement_type)
print("date:", statement.statement_date)
print("transactions:")
for t in statement.transactions:
    print(t)
print("count:", len(statement.transactions))
print("sum:", round(sum(t.amount for t in statement.transactions), 2))
