from tortoise import fields
from dipdup.models import Model


class Pool(Model):
    class Meta:
        table = 'pool'
    address = fields.CharField(max_length=42, pk=True, unique=True)
    id = fields.IntField()
    token_x = fields.ForeignKeyField('models.Token', "token_x_pools")
    token_y = fields.ForeignKeyField('models.Token', "token_y_pools")
    originated_at = fields.DatetimeField()


class Token(Model):
    class Meta:
        table = 'token'

    id = fields.IntField(pk=True)
    address = fields.TextField()
    token_id = fields.TextField(null=True)
    name = fields.TextField(null=True)
    symbol = fields.TextField(null=True)
    thumbnail_uri = fields.TextField(null=True)
    decimals = fields.IntField(null=True)


class Swap(Model):
    class Meta:
        table = 'swap'
        unique_together = ('id', 'timestamp')

    id = fields.IntField(pk=True, allows_generated=True)
    pool = fields.ForeignKeyField('models.Pool')
    hash = fields.CharField(64)
    dx = fields.DecimalField(100, 0)
    dy = fields.DecimalField(100, 0)
    is_x_to_y = fields.BooleanField()
    sender = fields.CharField(42)
    receiver = fields.CharField(42)
    timestamp = fields.DatetimeField()
