
class Warrior:
    def __init__(self, name:str, power: int, price: int, entity=None):
        self.name: str = name
        self.power: int = power
        self.entity = entity
        self.price: int = price
    def get_name(self):
        if self.entity is None:
            return "[b] "+self.name
        else:
            return "[P] "+self.name
    def get_power(self) -> int:
        return self.power
class Fraction:
    def __init__(self, name: str, x: int, y: int, player=None):
        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.open: bool = True
        self.warriors_types: list[Warrior] = [Warrior("Рядовой", 1, 10000), Warrior("Сержант", 3, 25000)]
        self.warriors = {self.warriors_types[0]: 10, self.warriors_types[1]: 0}
        self.owner: Player = player
        self.players: [Player] = []
        self.banned_players: [Player] = []
    def migrate(self, fraction, player):
        self.players.remove(player)
        player.fraction = fraction

    def getbase(self):
        return (self.x, self.y)
    def change_warrior_name(self, level: int, name: str):
        if self.warriors_types[level].entity is None:
            self.warriors_types[level].name = name
            return True
        return False
    def change_name(self, name: str):
        self.name = name

    def get_warrior(self, warrior: Warrior):
        for i in self.warriors:
            if i.get_name() == warrior.get_name():
                return i
        return False
    def remove_warrior(self, warrior: Warrior):
        if self.get_warrior(warrior):
            self.warriors_types.remove(warrior)
            del self.warriors[warrior]
            return True
        return False
    def kick_man(self, player) -> bool:
        for i in self.players:
            if player==i:
                self.players.remove(i)
                return True
        return False


class Item:
    def __init__(self, name: str, cost: int, count: int = 0):
        self.name: str = name
        self.cost: int = cost
        self.count = count
class Player:
    def __init__(self, user_id: int, fraction: Fraction, nickname: str = None):
        self.user_id: int = user_id
        self.name: str = nickname
        self.x, self.y = fraction.getbase()
        self.fraction: Fraction = fraction
        self.power = 2
        self.warriors = []
        self.backpack = []
        self.leader = 5
        self.balance: int = 100
        self.playable: bool = True
    def move(self, delta_x: int, delta_y: int):
        self.x += delta_x
        self.y += delta_y
    def change_playable(self, value: bool):
        self.playable = value
    def new_warrior(self, warrior: Warrior):
        self.warriors.append(warrior)
    def total_power(self) -> int:
        count = 0
        for i in self.warriors:
            count+=i.power
        return count
    def get_warriors(self) -> str:
        text = ""
        if len(self.warriors)==0:
            return "Никто)"
        i=0
        while i in range(len(self.warriors)):
            count=0
            sr: Warrior = self.warriors[i]
            for j in range(i, len(self.warriors), 1):
                sr_j: Warrior = self.warriors[j]
                if sr.name==sr_j.name and sr.power==sr_j.power:
                    count+=1
                    i+=1
            text+=f"{sr.name} - сила {sr.power} - количество {count}\n"
        return text
    def choose_warrior(self, warrior_name: str) -> Warrior:
        if len(self.warriors)==0:
            return KeyError
        for i in range(len(self.warriors)):
            if warrior_name==self.warriors[i].name:
                return self.warriors.pop(i)


class Map:

    class Sector:

        class Building:

            def __init__(self, name: str, owner: Player, building_type: str):
                self.name = name
                self.firstname: str = name
                self.owner = owner
                self.building_type = building_type
                self.items = [Item("Снюс", 300)]
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
        def get_defense(self) -> int:
            value: int = 0
            for i in self.warriors:
                value+=i.power
            return value
        def new_warrior(self, warrior: Warrior):
            self.warriors.append(warrior)

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
        self.map[y][x].warriors = []
        self.map[y][x].destroy()
    def annihilate_clan(self, fraction: Fraction):
        for y in range(self.size_y):
            for x in range(self.size_x):
                if self.map[y][x].fraction == fraction:
                    self.map[y][x].fraction=self.fraction_list[0]
        self.fraction_list.remove(fraction)
    def count_sectors(self, fraction: Fraction) -> int:
        counter: int = 0
        for y in range(self.size_y):
            for x in range(self.size_x):
                if self.map[y][x].fraction == fraction: counter+=1
        return counter

    def get_sector(self, x: int, y: int) -> Sector:
        return self.map[y][x]
    def create_clan(self, fraction: Fraction) -> Fraction:
        self.fraction_list.append(fraction)
        self.capture_sector(fraction, fraction.x, fraction.y)
        self.get_sector(fraction.y, fraction.x).build(Map.Sector.Building(f"База клана {fraction.name}", owner=fraction.owner, building_type="spawn"))
        return fraction