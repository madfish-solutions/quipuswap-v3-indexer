from typing import Any
from dipdup.context import HandlerContext
from dipdup.models.tezos import TezosTransaction
from quipuswap_v3_indexer.types.fa12_token.tezos_parameters.transfer import TransferParameter as Fa12TransferParameter
from quipuswap_v3_indexer.types.fa2_token.tezos_parameters.transfer import TransferParameter as Fa2TransferParameter
from quipuswap_v3_indexer.types.v3_pool.tezos_parameters.y_to_x import YToXParameter as YToXParameter
from quipuswap_v3_indexer.types.v3_pool.tezos_storage import V3PoolStorage

from quipuswap_v3_indexer.helpers import extract_amount

import quipuswap_v3_indexer.models as models
import quipuswap_v3_indexer.handlers.shared as shared


async def on_y_to_x(
    _ctx: HandlerContext,
    y_to_x: TezosTransaction[YToXParameter, V3PoolStorage],
    _token_y_transfer: TezosTransaction[Fa12TransferParameter | Fa2TransferParameter, Any],
    token_x_transfer: TezosTransaction[Fa12TransferParameter | Fa2TransferParameter, Any],
) -> None:
    pool_address = y_to_x.data.target_address

    await shared.update_sqrt_price(pool_address, y_to_x.storage.sqrt_price)
    await models.Swap.create(
        pool_id=pool_address,
        hash=y_to_x.data.hash,
        dx=extract_amount(token_x_transfer),
        dy=y_to_x.parameter.dy,
        sender=y_to_x.data.sender_address,
        receiver=y_to_x.parameter.to_dx,
        timestamp=y_to_x.data.timestamp,
        is_x_to_y=False,
    )
