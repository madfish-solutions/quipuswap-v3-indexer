import quipuswap_v3_indexer.models as models


async def update_sqrt_price(pool_address: str, sqrt_price: int) -> None:
    saved_pool = await models.Pool.get(address=pool_address)
    saved_pool.sqrt_price = sqrt_price
    await saved_pool.save()
