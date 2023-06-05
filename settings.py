import os
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.environ['BOT_TOKEN']
WEBHOOK_URL = os.environ['WEBHOOK_URL']
WEBAPP_HOST = os.environ['WEBAPP_HOST']
WEBAPP_PORT = os.environ['WEBAPP_PORT']
CHATGPT_ORGANIZATION = os.environ['CHATGPT_ORGANIZATION']
CHATGPT_TOKEN = os.environ['CHATGPT_TOKEN']
YOOKASSA_ID = os.environ['YOOKASSA_ID']
YOOKASSA_TOKEN = os.environ['YOOKASSA_TOKEN']
PRICES = {
  2_000: 12_00, # 6 rub / word
  10_000: 50_00, # 5 rub / word
  25_000: 100_00, # 4 rub / word
  50_000: 150_00, # 3 rub / word
  150_000: 300_00, # 2 rub / word
  300_000: 400_00, # 1.(3) rub / word
}
FREE_WORDS = 1000

REDIS = {
  'host': os.environ['REDIS_HOST'],
  'port': os.environ['REDIS_PORT'],
  'db': os.environ['REDIS_DB_NUMBER'],
  'username': os.environ['REDIS_USERNAME'],
  'password': os.environ['REDIS_PASSWORD'],
  'ssl': os.environ['REDIS_SSL_ENABLED'] == 'True',
}

# DB_URL = 'sqlite://db.sqlite3'
DB_URL = os.environ['DB_URL']

TORTOISE_ORM = {
  'connections': {'default': DB_URL},
  'apps': {
    'models': {
      'models': ['models', 'aerich.models'],
      'default_connection': 'default',
    }
  }
}
