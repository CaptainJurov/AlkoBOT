from config import keys
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from Modules import Classes
print("loaded")
Map = Classes.Map(100, 100)
Map.create_clan(Classes.Fraction("Хряки", 0, 0))
Map.create_clan(Classes.Fraction("Медведи", 1, 1))
players = {}
bot = Bot(token=keys)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
