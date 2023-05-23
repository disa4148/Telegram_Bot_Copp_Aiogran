import asyncio
import logging
import config

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage #Хранилище состояний

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
#bot = Bot(token=config.BOT_TOKEN)
bot = Bot(token='5826445945:AAGwHbEk5eklQu7BIOwszG84EALhWrzmCJw')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

