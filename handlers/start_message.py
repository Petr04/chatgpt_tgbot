from setup import dp, bot
from state import BotState
from settings import FREE_WORDS
from aiogram.types import \
  InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from aiogram.utils.deep_linking import decode_payload
from models import User, Chat
from utlis import format_number
from yookassa import Payment
import json


start_message_keyboard = InlineKeyboardMarkup() \
  .row(
    InlineKeyboardButton(
      'Подробнее о словах', callback_data='more_about_limits'),
    InlineKeyboardButton(
      'О возможностях ChatGPT', callback_data='more_about_features')
  )

def start_message_kwargs(name, user):
  return {
    'text':
      f'Здравствуйте, {name}! С помощью этого бота '
      'вы сможете использовать ChatGPT без ограничений и рекламы.\n\n'
      'Чтобы начать пользоваться ChatGPT, просто напишите боту.\n\n'
      '*Команды:*\n'
      '/buy — Купить слова\n'
      '/clean — Сбросить историю сообщений\n'
      '/balance — Посмотреть баланс\n'
      '/referral — Приведи друга и получи 1 000 слов\n'
      '/help — Помощь\n\n'
      f"*Баланс:* {format_number(user.balance)} слов",
    'parse_mode': ParseMode.MARKDOWN,
    'reply_markup': start_message_keyboard,
  }


async def manage_referee(user, referee):
  if await user.referee != None or user.id == referee.id:
    return

  user.referee = referee
  await user.save()

  referee.balance += 1000
  await referee.save()
  await bot.send_message(
    referee.id,
    'Вам начислено 1 000 слов за приведённого пользователя'
    f'*Баланс:* {format_number(referee.balance)} слов',
    parse_mode=ParseMode.MARKDOWN,
  )


async def manage_args(message):
  try:
    payload = json.loads(decode_payload(message.get_args()))
  except json.decoder.JSONDecodeError:
    return

  user, created = await User.get_or_create(id=message['from'].id)

  if 'referee' in payload and created:
    referee_id = payload['referee']
    referee = await User.get_or_none(id=int(referee_id))
    if referee:
      await manage_referee(user, referee)


@dp.message_handler(commands=['start', 'help'], state='*')
async def handle_start(message, state):
  await manage_args(message)
  # TODO: auto check balance

  user, _ = await User.get_or_create(id=message['from'].id)

  await message.answer(**start_message_kwargs(message.chat.first_name, user))
  await BotState.first()


async def show_info_page(message, text):
  keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton('Назад', callback_data='back_to_start_message'))

  await message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(text='more_about_limits', state='*')
async def handle_more_about_limits(callback):
  await show_info_page(
    callback.message,
    'При подсчёте использованных слов учитываются слова в вашем '
    'запросе и в ответе ChatGPT. Отдельно учитываются и слова в предыдущих сообщениях.\n\n'
    'Это необходимо, чтобы модель лучше понимала, о чём идёт разговор и выдавала более '
    'точные и полезные ответы, а вы легко могли задать вопрос, относящийся к обсуждаемой теме.\n\n'
    'Для экономии слов вы можете сбросить историю сообщений командой /clean.'
  )


@dp.callback_query_handler(text='more_about_features', state='*')
async def handle_more_about_limits(callback):
  await show_info_page(
    callback.message,
    'ChatGPT поможет вам почти с любым вопросом. Просто напишите его боту.\n\n'
    'Например, ChatGPT может\n'
    # '• ответить на вопрос,\n'
    # '• дать совет,\n'
    '• найти информацию,\n'
    '• написать текст,\n'
    # '• исправить или улучшить текст,\n'
    # '• качественно перевести текст,\n'
    '• посоветовать фильм,\n'
    '• предложить рецепт,\n'
    '• составить программу тренировок,\n'
    'и многое другое.'
  )


@dp.callback_query_handler(text='back_to_start_message', state='*')
async def handle_back_to_start_message(callback):
  user, _ = await User.get_or_create(id=callback.message.chat.id)
  await callback.message.edit_text(
    **start_message_kwargs(callback.message.chat.first_name, user))
