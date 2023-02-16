
from decimal import Decimal
from typing import Any
from dipdup.models import Transaction

from .types.fa12_token.parameter.transfer import TransferParameter


def extract_amount(transfer: Transaction[TransferParameter, Any]):
    if hasattr(transfer.parameter, 'value'):
        amount_out = transfer.parameter.value
    else:
        amount_out = sum(
            Decimal(tx.amount) for tx in transfer.parameter.__root__[0].txs
        )

    return amount_out
