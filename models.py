from tortoise.models import Model
from tortoise import fields
from settings import FREE_WORDS


class User(Model):
  id = fields.IntField(pk=True)
  balance = fields.IntField(default=FREE_WORDS)
  referee = fields.ForeignKeyField('models.User', related_name='referrals', null=True)


class Chat(Model):
  id = fields.IntField(pk=True)
  user = fields.ForeignKeyField('models.User')
  content = fields.JSONField(default={'messages': []})
