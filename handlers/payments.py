from setup import dp, bot
from state import BotState
from settings import (
  PRICES,
  YOOKASSA_ID,
  YOOKASSA_TOKEN,
)
from aiogram.types import (
  InlineKeyboardMarkup,
  InlineKeyboardButton,
  ParseMode,
  LabeledPrice,
)
from utlis import format_number
from aiogram.utils.deep_linking import get_start_link
import asyncio
import re
import uuid
from yookassa import Configuration, Payment
from models import User


Configuration.account_id = YOOKASSA_ID
Configuration.secret_key = YOOKASSA_TOKEN


def check_payment_status(payment_id):
  try:
    payment = Payment.find_one(payment_id)
  except:
    return None, 'error'

  amount = int(float(payment.amount.value))
  words = 0
  for words_lot, price in PRICES.items():
    if price // 100 == amount:
      words = words_lot
      break

  return words, payment.status


async def price_to_pair(words_number, price):
  payment = Payment.create({
    'amount': {
      'value': str(price / 100),
      'currency': 'RUB',
    },
    'confirmation': {
      'type': 'redirect',
      # 'return_url': await get_start_link({'payment': True}, encode=True),
      'return_url': 'https://t.me/chat_gpt_4_ru_bot',
    },
    'capture': True,
    'description': f'Купить {words_number} слов',
  }, uuid.uuid4())

  return payment, InlineKeyboardButton(
    f'{format_number(words_number)} '
    f'за {format_number(price // 100)} ₽',
    url=payment.confirmation.confirmation_url,
  )


async def buy(message, state, text):
  sent_message = await message.answer('Подождите...')

  payments, buttons = zip(*[await price_to_pair(words_number, price)
    for words_number, price in PRICES.items()])
  prices_keyboard = InlineKeyboardMarkup(row_width=2) \
    .add(*buttons)

  await sent_message.edit_text(
    text,
    reply_markup=prices_keyboard,
  )
  await message.answer('Интересный факт: в романе "Война и мир" около 500 000 слов')
  status_message = await message.answer(
    'После оплаты нажмите на кнопку',
    reply_markup=InlineKeyboardMarkup().add(
      InlineKeyboardButton('Я заплатил', callback_data='check_payment_status')
    )
  )

  await state.update_data(
    payment_ids=list(payment.id for payment in payments),
    message=status_message
  )


@dp.message_handler(commands=['buy'], state='*')
async def handle_buy(message, state):
  await buy(message, state, 'Сколько слов вы хотите купить?')


@dp.callback_query_handler(text='check_payment_status', state='*')
async def handle_check_status(callback, state):
  user, _ = await User.get_or_create(id=callback.message.chat.id)
  data = await state.get_data()
  for payment_id in data['payment_ids']:
    words, status = check_payment_status(payment_id)

    if status == 'succeeded':
      user.balance = user.balance + words
      await user.save()
      await bot.edit_message_text(
        f'Оплата прошла успешно. '
        f'На ваш баланс начислено {format_number(words)} слов.\n'
        f'*Баланс:* {format_number(user.balance)} слов',
        parse_mode=ParseMode.MARKDOWN,
        chat_id=data['message'].chat.id,
        message_id=data['message'].message_id,
      )
      break
    
    if status == 'error':
      await bot.edit_message_text(
        'Извините, что-то пошло не так. Чтобы решить вопрос, обращайтесь к @piotr_makarov.',
        chat_id=data['message'].chat.id,
        message_id=data['message'].message_id,
        reply_markup=InlineKeyboardMarkup().add(
          InlineKeyboardButton('Попробовать ещё раз', callback_data='check_payment_status')
        ),
      )
      break

  else:
    await bot.edit_message_text(
      'Пока деньги не пришли. Попробуйте проверить чуть позже.',
      chat_id=data['message'].chat.id,
      message_id=data['message'].message_id,
      reply_markup=InlineKeyboardMarkup().add(
        InlineKeyboardButton('Попробовать ещё раз', callback_data='check_payment_status')
      ),
    )

