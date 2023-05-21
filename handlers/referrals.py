from setup import dp
from models import User
from aiogram.utils.deep_linking import get_start_link
import json


@dp.message_handler(commands=['referral'], state='*')
async def referral_handler(message):
  user, _ = await User.get_or_create(id=message['from'].id)

  link = await get_start_link(json.dumps({'referee': user.id}), encode=True)
  await message.answer(
    f'Вы можете пригласить человека по ссылке {link} '
    'и получить 1 000 слов в подарок'
  )
