from setup import dp, Bot, bot
from state import BotState
from datetime import datetime
from models import User, Chat
from .payments import buy
import threading
import asyncio
import openai


model = 'gpt-3.5-turbo'
current_date = datetime.now().strftime('%Y-%m-%d')
system_message = {
  'role': 'system',
  'content':
    'You are ChatGPT, a large language model trained by OpenAI. '
    'Answer as concisely as possible.\nKnowledge cutoff: 2021-09-01\n'
    f'Current date: {current_date}',
}


def count_words(text):
  return len(text.split())


@dp.message_handler(commands=['clean'], state='*')
async def handle_clean(message, state):
  chat = await Chat.get(user=message['from'].id)
  chat.content['messages'] = []
  await message.answer('История сообщений сброшена')
  await chat.save()


@dp.message_handler(state='*')
async def handle_prompt(message, state):
  user_message = {
    'role': 'user',
    'content': message.text,
  }

  user, _ = await User.get_or_create(id=message['from'].id)

  if user.balance <= 0:
    await buy(message, state, 'У вас недостаточно слов. Вы можете купить ещё')
    return

  chat, is_chat_new = await Chat.get_or_create(user=user)

  if is_chat_new:
    chat.content['messages'].append(system_message)

  answer = await message.answer('Подождите...')

  loop = asyncio.get_event_loop()

  def request_answer(loop):
    try:
      completion = openai.ChatCompletion.create(
        model=model,
        messages=chat.content['messages'],
      )
    except openai.error.InvalidRequestError as exception:
      if exception.args[0].startswith("This model's maximum context length is"):
        print('too long')
        del chat.content['messages'][1:3]
        return request_answer(loop)
      else:
        print('unknown error:', exception)
        asyncio.run_coroutine_threadsafe(answer.edit_text('Произошла неизвестная ошибка'), loop)
        return None

    return completion

  def completion_function(loop):
    chat.content['messages'].append(user_message)
    completion = request_answer(loop)
    if completion == None:
      return

    assistant_message = completion.choices[0].message

    words_used = count_words(message.text) + count_words(assistant_message.content)
    user.balance -= words_used

    Bot.set_current(bot)

    asyncio.run_coroutine_threadsafe(answer.edit_text(assistant_message.content), loop)
    chat.content['messages'].append(assistant_message.to_dict())
    asyncio.run_coroutine_threadsafe(chat.save(), loop)
    asyncio.run_coroutine_threadsafe(user.save(), loop)
    print(chat.content['messages'])

  thread = threading.Thread(target=completion_function, args=[loop])
  thread.start()
