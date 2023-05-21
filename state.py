from aiogram.dispatcher.filters.state import State, StatesGroup


class BotState(StatesGroup):
  Start = State()
  Money = State()
