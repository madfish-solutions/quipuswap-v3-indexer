from dipdup.context import HandlerContext
from dipdup.models import Origination
from quipuswap_v3_indexer.types.v3_pool.storage import V3PoolStorage


async def on_pool_origination(
    ctx: HandlerContext,
    v3_pool_origination: Origination[V3PoolStorage],
) -> None:
    ...
