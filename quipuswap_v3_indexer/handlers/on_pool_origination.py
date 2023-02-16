from dipdup.context import HandlerContext
from dipdup.models import OperationData

import requests

import quipuswap_v3_indexer.models as models


def get_metadata(address, token_id=None):
    actual_token_id = token_id if token_id is not None else '0'
    return requests.get(
        f'https://metadata.templewallet.com/metadata/{address}/{actual_token_id}'
    ).json()


async def get_or_create_token(raw_token):
    token_id = None

    if 'fa12' in raw_token:
        token_address = raw_token['fa12']
    else:
        token_address = raw_token['fa2']['token_address']
        token_id = raw_token['fa2']['token_id']

    token = await models.Token.get_or_none(
        address=token_address,
        token_id=token_id
    )

    if token is None:
        metadata = get_metadata(token_address, token_id)
        token = await models.Token.create(
            address=token_address,
            token_id=token_id,
            name=metadata['name'],
            symbol=metadata['symbol'],
            decimals=metadata['decimals']
        )

    return token


async def on_pool_origination(
    ctx: HandlerContext,
    v3_pool_origination: OperationData,
) -> None:
    pool_address = v3_pool_origination.originated_contract_address

    token_x = await get_or_create_token(v3_pool_origination.storage['constants']['token_x'])
    token_y = await get_or_create_token(v3_pool_origination.storage['constants']['token_y'])

    await models.Pool.create(
        address=pool_address,
        token_x_id=token_x.id,
        token_y_id=token_y.id,
    )

    if pool_address not in ctx.config.contracts:
        await ctx.add_contract(
            name=pool_address,
            address=pool_address,
            typename='v3_pool'
        )

    if token_x.address not in ctx.config.contracts:
        await ctx.add_contract(
            name=token_x.address,
            address=token_x.address,
            typename='fa12_token' if token_x.token_id is None else 'fa2_token'
        )

    if token_y.address not in ctx.config.contracts:
        await ctx.add_contract(
            name=token_y.address,
            address=token_y.address,
            typename='fa12_token' if token_y.token_id is None else 'fa2_token'
        )

    await ctx.add_index(f'swaps_{pool_address}', 'swaps', {
        'pool': pool_address,
        'token_x': token_x.address,
        'token_y': token_y.address,
    })
