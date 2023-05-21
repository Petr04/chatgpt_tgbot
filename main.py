import handlers
from setup import dp
from settings import *
from aiogram import executor


if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)
