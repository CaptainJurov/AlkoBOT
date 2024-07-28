from Modules import Classes
def capture(player: Classes.Player, sector: Classes.Map.Sector):
    print(len(player.warriors), len(sector.warriors))
    player_atk = player.total_power()+player.power
    sector_def = sector.get_defense()
    player_count = 1 + len(player.warriors)
    sector_count = len(sector.warriors)
    power_count_defender = player_atk/sector_count
    power_count_attacker = sector_def/player_count
    i: Classes.Warrior
    for i in sector.warriors:
        if i.get_power()<=power_count_defender:
            sector.warriors.remove(i)
    for i in player.warriors:
        if i.get_power()<=power_count_attacker:
            player.warriors.remove(i)
    print(len(sector.warriors), sector.warriors)
    print(len(player.warriors), player.warriors)

if __name__=="__main__":
    fraca = Classes.Fraction("goyda", 1, 1)
    fraca_s = Classes.Fraction("Zydaa", 2, 1)
    player = Classes.Player(228, fraca, nickname="GOOOAL")
    player.new_warrior(Classes.Warrior("ZOV", 3, 1))
    sector = Classes.Map.Sector(1,1, fraca_s)
    sector.basic_def = 3
    for i in range(10):
        player.new_warrior(Classes.Warrior("ZOV", 1, 1))
        sector.new_warrior(Classes.Warrior("ZOV", 3, 1))
    capture(player, sector)