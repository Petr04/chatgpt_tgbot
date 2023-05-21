import handlers
from setup import bot, dp
from aiohttp import web
from settings import *
from aiogram import executor
from aiogram.types import Update


async def on_startup(_):
  await bot.set_webhook(f'{WEBHOOK_URL}/{BOT_TOKEN}')
  # await bot.set_webhook(f'/{BOT_TOKEN}')


async def on_shutdown(_):
  pass


async def handle_webhook(request):
  url = str(request.url)
  index = url.rfind('/')
  token = url[index+1:] # this method is used because in some cases request object can't be correctly interpreted and match_info will return empty object
  if token == BOT_TOKEN:
    update = Update(**await request.json()) # we just parse our bytes into dictionary
    await dp.process_update(update) # this will just process update using the appropriate handler
    return web.Response() # construct the response object

  return web.Response(status=403) # if our TOKEN is not authenticated


app = web.Application()
app.router.add_post(f'/{BOT_TOKEN}', handle_webhook)


if __name__ == '__main__':
  app.on_startup.append(on_startup)
  app.on_shutdown.append(on_shutdown)
  print(WEBAPP_PORT)
  
  web.run_app(
    app,
    host=WEBAPP_HOST,
    port=WEBAPP_PORT,
  )

# if __name__ == '__main__':
#   executor.start_polling(dp, skip_updates=True)
