from setup import dp
from models import User
from aiogram.types import ParseMode


@dp.message_handler(commands=['balance'], state='*')
async def balance_handler(message):
  user, _ = await User.get_or_create(id=message['from'].id)
  await message.answer(
    f'*Баланс:* {user.balance} слов',
    parse_mode=ParseMode.MARKDOWN,
  )
