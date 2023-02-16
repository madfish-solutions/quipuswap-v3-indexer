from tortoise import fields
from dipdup.models import Model


class Pool(Model):
    class Meta:
        table = 'pool'

    address = fields.CharField(max_length=42, pk=True)
    token_x = fields.ForeignKeyField('models.Token', "token_x_pools")
    token_y = fields.ForeignKeyField('models.Token', "token_y_pools")


class Token(Model):
    class Meta:
        table = 'token'

    id = fields.IntField(pk=True)
    address = fields.TextField()
    token_id = fields.TextField(null=True)
    name = fields.TextField(null=True)
    symbol = fields.TextField(null=True)
    decimals = fields.IntField()


class Swap(Model):
    class Meta:
        table = 'swap'
        unique_together = ('id', 'timestamp')

    id = fields.IntField(pk=True, allows_generated=True)
    pool = fields.ForeignKeyField('models.Pool')
    from_token = fields.ForeignKeyField('models.Token', "from_token_swaps")
    to_token = fields.ForeignKeyField('models.Token', "to_token_swaps")
    hash = fields.CharField(64)
    amount_in = fields.DecimalField(100, 0)
    amount_out = fields.DecimalField(100, 0)
    sender = fields.CharField(42)
    receiver = fields.CharField(42)
    timestamp = fields.DatetimeField()
