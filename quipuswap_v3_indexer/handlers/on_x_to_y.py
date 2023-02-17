from typing import Any
from dipdup.context import HandlerContext
from dipdup.models import Transaction
from quipuswap_v3_indexer.types.fa12_token.parameter.transfer import TransferParameter as Fa12TransferParameter
from quipuswap_v3_indexer.types.fa12_token.storage import Fa12TokenStorage
from quipuswap_v3_indexer.types.fa2_token.parameter.transfer import TransferParameter as Fa2TransferParameter
from quipuswap_v3_indexer.types.fa2_token.storage import Fa2TokenStorage
from quipuswap_v3_indexer.types.v3_pool.parameter.x_to_y import XToYParameter as XToYParameter
from quipuswap_v3_indexer.types.v3_pool.storage import V3PoolStorage

from quipuswap_v3_indexer.helpers import extract_amount

import quipuswap_v3_indexer.models as models


async def on_x_to_y(
    _ctx: HandlerContext,
    x_to_y: Transaction[XToYParameter, V3PoolStorage],
    _token_x_transfer: Transaction[Fa12TransferParameter | Fa2TransferParameter, Any],
    token_y_transfer: Transaction[Fa12TransferParameter | Fa12TransferParameter, Any],
) -> None:
    pool_address = x_to_y.data.target_address

    await models.Swap.create(
        pool_id=pool_address,
        hash=x_to_y.data.hash,
        dx=x_to_y.parameter.dx,
        dy=extract_amount(token_y_transfer),
        sender=x_to_y.data.sender_address,
        receiver=x_to_y.parameter.to_dy,
        timestamp=x_to_y.data.timestamp,
        is_x_to_y=True,
    )
