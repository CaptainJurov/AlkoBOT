from config import keys
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
print("loaded")
bot = Bot(token=keys)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
