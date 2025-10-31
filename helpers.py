
from decimal import Decimal
from typing import Any
from dipdup.models.tezos import TezosTransaction

from .types.fa12_token.tezos_parameters.transfer import TransferParameter as Fa12TransferParameter
from .types.fa2_token.tezos_parameters.transfer import TransferParameter as Fa2TransferParameter


def extract_amount(transfer: TezosTransaction[Fa12TransferParameter | Fa2TransferParameter, Any]):
    if hasattr(transfer.parameter, 'value'):
        amount_out = transfer.parameter.value
    else:
        amount_out = sum(
            Decimal(tx.amount) for tx in transfer.parameter.root[0].txs
        )

    return amount_out
