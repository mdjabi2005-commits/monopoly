"""Parser for La Banque Postale (LBP) bank statements.

Relevé de compte courant format:
- Monthly statements
- 2 columns: Débit (¤) / Crédit (¤)
- Transaction dates: DD/MM (year inferred from statement date)
- Amounts in French format: 350,00 or 1 234,56
"""

import re

from monopoly.banks.base import BankBase
from monopoly.config import MultilineConfig, StatementConfig
from monopoly.constants import EntryType
from monopoly.constants.date import ISO8601
from monopoly.identifiers import MetadataIdentifier, TextIdentifier

FRENCH_AMOUNT = r"(?P<amount>\d{1,3}(?:[\s\xa0\u202f]\d{3})*,\d{2})"


class LaBanquePostale(BankBase):
    """La Banque Postale current account (CCP) debit statement parser."""

    name = "la_banque_postale"

    debit = StatementConfig(
        statement_type=EntryType.DEBIT,
        # Relevé édité le 09 juillet 2026 or Situation de vos comptes au 8 juillet 2026
        statement_date_pattern=re.compile(
            r"Relevé\s+édité\s+le\s+(\d{1,2}\s+[a-zA-Zà-ÿ]+\s+\d{4})"
        ),
        # Column header line: "Date  Opérations  Débit (¤)  Crédit (¤)"
        header_pattern=re.compile(
            r"(Date\s+Opérations\s+Débit.*)",
            re.IGNORECASE,
        ),
        # Transaction line: "15/06  CARTE X0486 14/06/26 A 18H58  350,00"
        transaction_pattern=re.compile(
            rf"^\s*(?P<transaction_date>{ISO8601.DD_MM})\s+"
            + r"(?P<description>.+?)\s+"
            + FRENCH_AMOUNT
            + r"\s*$"
        ),
        transaction_date_format="%d/%m",
        multiline_config=MultilineConfig(multiline_descriptions=True),
        safety_check=False,
    )

    identifiers = [
        [
            TextIdentifier("LA BANQUE POSTALE"),
        ],
        [
            TextIdentifier("La Banque Postale"),
        ],
        [
            TextIdentifier("Compte Courant Postal"),
        ],
    ]

    statement_configs = [debit]
