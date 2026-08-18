"""Parser for Sumeria bank statements.

Relevé de compte format:
- Compte courant avec colonnes Débit / Crédit / Solde
- Période: "Période du 01/07/2026 au 31/07/2026"
- Dates opération/confirmation: JJ/MM
- Description multiligne possible
- Montants dans des colonnes séparées, sans signe
"""

import re

from monopoly.banks.base import BankBase
from monopoly.config import MultilineConfig, StatementConfig
from monopoly.constants.date import ISO8601
from monopoly.identifiers import MetadataIdentifier, TextIdentifier
from monopoly.constants import EntryType


class Sumeria(BankBase):
    """Sumeria current account (compte courant) debit statement parser."""

    name = "sumeria"

    debit = StatementConfig(
        statement_type=EntryType.DEBIT,
        statement_date_pattern=re.compile(
            rf"Période du \d{{2}}/\d{{2}}/\d{{4}} au ({ISO8601.DD_MM_YYYY})"
        ),
        header_pattern=re.compile(r"Débit\s+Crédit"),
        transaction_pattern=re.compile(
            r"^\s*(?P<transaction_date>\d{2}/\d{2})\s+"
            r"\d{2}/\d{2}\s+"
            r"(?P<description>.+?)\s{2,}"
            r"(?P<amount>\d+\.\d{2})\s+"
            r"\d+\.\d{2}\s*$"
        ),
        transaction_date_format="%d/%m",
        multiline_config=MultilineConfig(multiline_descriptions=True),
        safety_check=False,
    )

    identifiers = [
        [TextIdentifier("Sumeria")],
        [MetadataIdentifier(producer="pdfcpu")],
    ]

    statement_configs = [debit]
