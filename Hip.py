from config import keys
from aiogram import Bot, Dispatcher
import aiogram
from aiogram.fsm.storage.memory import MemoryStorage
from Modules import Classes, Timer
print("loaded")
Clock = Timer.Timer()
glob_room = Classes.Room()
Map = Classes.Map(100, 100)

class Building:
    def __init__(self, name: str, type: str, price: int):
        self.name: str = name
        self.type: str = type
        self.price: int = price
buildings = {
    "Завод" :Building("Завод", "work", 100_000_000),
    "Магазин": Building("Магазин", "shop", 10_000_000),
    "Банк": Building("Банк", "bank", 1_000_000_000),
    "Шахта": Building("Шахта", "mine", 100_000_000),
    "Казино": Building("Казино", "casino", 1_000_000_000),
    "Дорога": Building("Дорога", "road", 10_000_000),
    "Призывной пункт": Building("Призывной пункт", "warriors", 100_000_000),
    "Бесполезная постройка": Building("Фонтан", "useless", 1_000_000)
}

buildings_for_types = {}
for i in buildings:
    buildings_for_types[buildings[i].type] = buildings[i]
def get_all():
    text = ""
    for i in buildings:
        text+=f"{buildings[i].name} - стоит {buildings[i].price:,} шекелей\n"
    return text
players = {0: Classes.Player(0, Map.fraction_list[0], "Server")}
Map.create_clan(Classes.Fraction("Хряки", 0, 0, player=players[0]))
Map.create_clan(Classes.Fraction("Медведи", 1, 1, player=players[0]))
class Interact(aiogram.filters.state.StatesGroup):
    interact = aiogram.filters.state.State()
    choosing = aiogram.filters.state.State()
    enter = aiogram.filters.state.State()
    build = aiogram.filters.state.State()
    work = aiogram.filters.state.State()
    capture = aiogram.filters.state.State()
    warriors = aiogram.filters.state.State()

rooms: [Classes.Room] = []
storaga = {}
kicked = []
banned = []
bot = Bot(token=keys)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
