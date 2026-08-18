"""Parser for Trade Republic bank statements (Relevé de compte / Compte d'espèces).

Statement format:
- Multi-page document
- Columns: DATE | TYPE | DESCRIPTION | ENTRÉE D'ARGENT | SORTIE D'ARGENT | SOLDE
- Running balance at the end of each transaction line
- Period: e.g. "DATE  01 sept. 2025 - 13 juin 2026"
"""

import re

from monopoly.banks.base import BankBase
from monopoly.config import MultilineConfig, StatementConfig
from monopoly.constants import EntryType
from monopoly.constants.date import ISO8601
from monopoly.identifiers import MetadataIdentifier, TextIdentifier

FRENCH_AMOUNT = r"(?P<amount>\d{1,3}(?:[\s\xa0\u202f]\d{3})*,\d{2})"
FRENCH_BALANCE = r"(?P<balance>\d{1,3}(?:[\s\xa0\u202f]\d{3})*,\d{2})"


class TradeRepublic(BankBase):
    """Trade Republic cash account debit statement parser."""

    name = "trade_republic"

    debit = StatementConfig(
        statement_type=EntryType.DEBIT,
        # Period end date: "DATE  01 sept. 2025 - 13 juin 2026"
        statement_date_pattern=re.compile(
            r"DATE\s+\d{1,2}\s+[a-zA-Zà-ÿ.]+\s+\d{4}\s*-\s*(\d{1,2}\s+[a-zA-Zà-ÿ.]+\s+\d{4})"
        ),
        # Column header line: "DATE  TYPE  DESCRIPTION  ENTRÉE D'ARGENT  SORTIE D'ARGENT  SOLDE"
        header_pattern=re.compile(
            r"(DATE\s+TYPE\s+DESCRIPTION.*)",
            re.IGNORECASE,
        ),
        # Transaction line with amount and running balance
        transaction_pattern=re.compile(
            r"^\s*(?:(?P<transaction_date>\d{2}\s+[a-zA-Zà-ÿ.]+(?:\s+\d{4})?)\s+)?"
            + r"(?P<description>.+?)\s+"
            + FRENCH_AMOUNT
            + r"\s*€\s+"
            + FRENCH_BALANCE
            + r"\s*€\s*$"
        ),
        multiline_config=MultilineConfig(
            multiline_descriptions=True,
            multiline_transaction_date=True,
        ),
        safety_check=False,
    )

    identifiers = [
        [
            TextIdentifier("TRADE REPUBLIC BANK GMBH"),
        ],
        [
            TextIdentifier("Trade Republic Bank GmbH"),
        ],
        [
            TextIdentifier("traderepublic.fr"),
        ],
    ]

    statement_configs = [debit]
