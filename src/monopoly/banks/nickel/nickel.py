"""Parser for Nickel (Financière des Paiements Électroniques) bank statements.

Relevé de compte format:
- 1 page per month
- Signed amounts: -4,64 € (debit) / 700,00 € (credit)
- Date format: DD/MM/YYYY
- Statement period: "Du 01/07/2026 au 31/07/2026"
"""

import re

from monopoly.banks.base import BankBase
from monopoly.config import MultilineConfig, StatementConfig
from monopoly.constants import EntryType
from monopoly.constants.date import ISO8601
from monopoly.identifiers import MetadataIdentifier, TextIdentifier

FRENCH_AMOUNT = r"(?P<polarity>-)?(?P<amount>\d{1,3}(?:[\s\xa0\u202f]\d{3})*,\d{2})"


class Nickel(BankBase):
    """Nickel current account (compte courant) debit statement parser."""

    name = "nickel"

    debit = StatementConfig(
        statement_type=EntryType.DEBIT,
        # Capture the end date of the statement period: "Du 01/07/2026 au 31/07/2026"
        statement_date_pattern=re.compile(
            rf"au\s+({ISO8601.DD_MM_YYYY})"
        ),
        # Column header line: "N°  DATE  TYPE D'OPÉRATION  LIBELLÉ  MONTANT"
        header_pattern=re.compile(
            r"(N°\s+DATE\s+TYPE)"
        ),
        # Transaction line: "  1  02/07/2026  ACHAT  WWW.VOISCOOTERS.COM PARIS  -4,64 €"
        transaction_pattern=re.compile(
            rf"^\s*(?:\d+\s+)?(?P<transaction_date>{ISO8601.DD_MM_YYYY})\s+"
            + r"(?P<description>.+?)\s+"
            + FRENCH_AMOUNT
            + r"\s*€?\s*$"
        ),
        transaction_date_format="%d/%m/%Y",
        multiline_config=MultilineConfig(multiline_descriptions=True),
        safety_check=False,
    )

    identifiers = [
        [
            TextIdentifier("Nickel"),
            MetadataIdentifier(producer="openhtmltopdf.com"),
        ]
    ]

    statement_configs = [debit]
