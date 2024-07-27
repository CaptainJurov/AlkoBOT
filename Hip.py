from config import keys
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from Modules import Classes
print("loaded")
Map = Classes.Map(100, 100)
class Building:
    def __init__(self, name: str, type: str, price: int):
        self.name = name
        self.type = type
        self.price = price
buildings = {
    "Завод" :Building("Завод", "work", 100_000_000),
    "Магазин": Building("Магазин", "shop", 10_000_000),
    "Банк": Building("Банк", "bank", 1_000_000_000),
    "Шахта": Building("Шахта", "mine", 100_000_000),
    "Казино": Building("Казино", "casino", 1_000_000_000),
    "Дорога": Building("Дорога", "road", 10_000_000)
}
def get_all():
    text = ""
    for i in buildings:
        text+=f"{buildings[i].name} - стоит {buildings[i].price:,} шекелей\n"
    return text
players = {0: Classes.Player(0, Map.fraction_list[0], "Server")}
Map.create_clan(Classes.Fraction("Хряки", 0, 0, player=players[0]))
Map.create_clan(Classes.Fraction("Медведи", 1, 1, player=players[0]))

bot = Bot(token=keys)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
