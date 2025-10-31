from typing import Any
from dipdup.context import HandlerContext
from dipdup.models.tezos import TezosTransaction
from quipuswap_v3_indexer.types.fa12_token.tezos_parameters.transfer import TransferParameter as Fa12TransferParameter
from quipuswap_v3_indexer.types.fa2_token.tezos_parameters.transfer import TransferParameter as Fa2TransferParameter
from quipuswap_v3_indexer.types.v3_pool.tezos_parameters.x_to_y import XToYParameter as XToYParameter
from quipuswap_v3_indexer.types.v3_pool.tezos_storage import V3PoolStorage

from quipuswap_v3_indexer.helpers import extract_amount

import quipuswap_v3_indexer.models as models
import quipuswap_v3_indexer.handlers.shared as shared


async def on_x_to_y(
    _ctx: HandlerContext,
    x_to_y: TezosTransaction[XToYParameter, V3PoolStorage],
    _token_x_transfer: TezosTransaction[Fa12TransferParameter | Fa2TransferParameter, Any],
    token_y_transfer: TezosTransaction[Fa12TransferParameter | Fa12TransferParameter, Any],
) -> None:
    pool_address = x_to_y.data.target_address

    await shared.update_sqrt_price(pool_address, x_to_y.storage.sqrt_price)
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
