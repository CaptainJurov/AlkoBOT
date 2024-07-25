
class Warrior:
    def __init__(self, name:str, power: int, price: int, entity=None):
        self.name = name
        self.power = power
        self.entity = None
        self.price = price
class Fraction:
    def __init__(self, name: str, x: int, y: int):
        self.name = name
        self.x = x
        self.y = y
        #self.warriors_types = {Warrior("Рядовой", 1, 10000): 0, Warrior("Сержант", 3, 25000): 0}
        self.warriors_types = [Warrior("Рядовой", 1, 10000), Warrior("Сержант", 3, 25000)]
        self.warriors = {self.warriors_types[0]: 10, self.warriors_types[1]: 0}
    def getbase(self):
        return (self.x, self.y)
    def change_name(self, level: int, name: str):
        self.warriors_types[level].name = name


class Item:
    def __init__(self, name):
        self.name = name
class Player:
    def __init__(self, user_id: int, fraction: Fraction):
        self.user_id = user_id
        self.x, self.y = fraction.getbase()
        self.fraction = fraction
        self.power = 1
        self.balance = 100
    def move(self, delta_x, delta_y):
        self.x += delta_x
        self.y += delta_y


class Map:

    class Sector:

        class Building:
            def __init__(self, name: str, owner: Player, building_type: str):
                self.name = name
                self.owner = owner
                self.building_type = building_type
                self.items = []
                self.materia_count = 10
            def add_item(self, item: Item):
                self.items.append(item)
            def get_items(self):
                return self.items

        #дополнительно - карта высот
        def __init__(self, x: int, y: int, fraction: Fraction):
            self.x = x
            self.y = y
            self.warriors = []
            self.building = self.Building("Ничего", None, "void")
            self.fraction = fraction
            self.basic_def = 1
            #ЗАВИСИТ ОТ ВЫСОТЫ
        def build(self, build: Building):
            self.building = build
        def destroy(self):
            self.building = self.Building("Ничего", None, "void")
    def __init__(self, size_x: int, size_y: int):
        #создание и заполнение карты
        #генерация ландшафта
        self.size_x = size_x
        self.size_y = size_y
        self.map = []

        self.fraction_list = [Fraction("None", -1, -1)]
        for y in range(size_y):
            temp = []
            for x in range(size_x):
                temp.append(Map.Sector(x, y, self.fraction_list[0]))
            self.map.append(temp)

    def capture_sector(self, winner: Fraction, x: int, y: int, ):
        if self.map[y][x].fraction.getbase()==(x, y):
            self.annihilate_clan(self.map[y][x].fraction)
        self.map[y][x].fraction = winner
    def annihilate_clan(self, fraction: Fraction):
        for y in range(self.size_y):
            for x in range(self.size_x):
                if self.map[y][x].fraction == fraction:
                    self.map[y][x].fraction=self.fraction_list[0]
        self.fraction_list.remove(fraction)

    def get_sector(self, x: int, y: int):
        return self.map[y][x]
    def create_clan(self, fraction: Fraction):
        self.fraction_list.append(fraction)
        self.capture_sector(fraction, fraction.x, fraction.y)



#тестинг)
map = Map(20, 10)
map.capture_sector(map.fraction_list[0], 9, 9)
map.create_clan(Fraction(name="Гойда", x=9, y=9))
clan = map.fraction_list[1]
clan.change_name(0, "Шкебеде сральник")
for i in map.map:
    text=""
    for j in i:
        text+=j.fraction.name[0]
    print(text)
print(map.get_sector(9,8).building.building_type)
for i in map.fraction_list[1].warriors:
    print(i.name)