from dipdup.context import HandlerContext
from dipdup.models.tezos import TezosOperationData
from dipdup.models.tezos import TezosTransaction

import requests

import quipuswap_v3_indexer.models as models
from quipuswap_v3_indexer.types.v3_factory.tezos_parameters.deploy_pool import DeployPoolParameter
from quipuswap_v3_indexer.types.v3_factory.tezos_storage import V3FactoryStorage


async def on_pool_origination(
    ctx: HandlerContext,
    deploy_pool: TezosTransaction[DeployPoolParameter, V3FactoryStorage],
    v3_pool_origination: TezosOperationData,
) -> None:
    pool_address = v3_pool_origination.originated_contract_address

    token_x = await get_or_create_token(v3_pool_origination.storage['constants']['token_x'])
    token_y = await get_or_create_token(v3_pool_origination.storage['constants']['token_y'])

    await models.Pool.create(
        address=pool_address,
        id=int(deploy_pool.storage.pool_count) - 1,
        token_x_id=token_x.id,
        token_y_id=token_y.id,
        sqrt_price=v3_pool_origination.storage['sqrt_price'],
        originated_at=v3_pool_origination.timestamp,
    )

    if pool_address not in ctx.config.contracts:
        await ctx.add_contract(
            name=pool_address,
            address=pool_address,
            typename='v3_pool',
            kind="tezos"
        )

    if token_x.address not in ctx.config.contracts:
        await ctx.add_contract(
            name=token_x.address,
            address=token_x.address,
            typename='fa12_token' if token_x.token_id is None else 'fa2_token',
            kind="tezos"
        )

    if token_y.address not in ctx.config.contracts:
        await ctx.add_contract(
            name=token_y.address,
            address=token_y.address,
            typename='fa12_token' if token_y.token_id is None else 'fa2_token',
            kind="tezos"
        )

    await ctx.add_index(f'swaps_{pool_address}', 'swaps', {
        'pool': pool_address,
        'token_x': token_x.address,
        'token_y': token_y.address,
    })


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
            name=metadata.get('name') or "Unknown Token",
            symbol=metadata.get('symbol') or "UNKNOWN",
            decimals=metadata.get('decimals') or 0,
            thumbnail_uri=metadata.get('thumbnailUri') or "",
        )

    return token


def get_metadata(address, token_id=None):
    actual_token_id = token_id if token_id is not None else '0'
    return requests.get(
        f'https://metadata.templewallet.com/metadata/{address}/{actual_token_id}'
    ).json()

