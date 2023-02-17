from dipdup.context import HandlerContext
from dipdup.models import Transaction
from quipuswap_v3_indexer.types.fa12_token.parameter.transfer import TransferParameter as YToXTransferFa12Parameter
from quipuswap_v3_indexer.types.fa12_token.storage import Fa12TokenStorage
from quipuswap_v3_indexer.types.fa2_token.parameter.transfer import TransferParameter as YToXTransferFa2Parameter
from quipuswap_v3_indexer.types.fa2_token.storage import Fa2TokenStorage
from quipuswap_v3_indexer.types.v3_pool.parameter.y_to_x import YToXParameter as YToXParameter
from quipuswap_v3_indexer.types.v3_pool.storage import V3PoolStorage

from quipuswap_v3_indexer.helpers import extract_amount

import quipuswap_v3_indexer.models as models


async def on_y_to_x(
    _ctx: HandlerContext,
    y_to_x: Transaction[YToXParameter, V3PoolStorage],
    _token_y_transfer: Transaction[YToXTransferFa12Parameter, Fa12TokenStorage],
    token_x_transfer: Transaction[YToXTransferFa2Parameter, Fa2TokenStorage],
) -> None:
    pool_address = y_to_x.data.target_address

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
