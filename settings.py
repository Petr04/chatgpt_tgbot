import os
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
WEBHOOK_URL = 'https://2fb2-31-162-127-244.ngrok-free.app'
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 8000
CHATGPT_ORGANIZATION = os.environ.get('CHATGPT_ORGANIZATION')
CHATGPT_TOKEN = os.environ.get('CHATGPT_TOKEN')
YOOKASSA_ID = os.environ.get('YOOKASSA_ID')
YOOKASSA_TOKEN = os.environ.get('YOOKASSA_TOKEN')
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
  'host': 'hot-kitten-30576.upstash.io',
  'port': 30576,
  'db': 0,
  'username': 'default',
  'password': os.environ.get('REDIS_PASSWORD'),
  'ssl': True,
}

# DB_URL = 'sqlite://db.sqlite3'
DB_URL = os.environ.get('DB_URL')

TORTOISE_ORM = {
  'connections': {'default': DB_URL},
  'apps': {
    'models': {
      'models': ['models', 'aerich.models'],
      'default_connection': 'default',
    }
  }
}
