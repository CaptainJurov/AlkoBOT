from Modules import Classes
import Hip
def capture(player: Classes.Player, sector: Classes.Map.Sector):
    player_atk = player.total_power()+player.power
    sector_def = sector.get_defense()*sector.basic_def
    player_count = len(player.warriors)+1
    sector_count = len(sector.warriors)
    if sector_count==0:
        Hip.Map.capture_sector(player.fraction, player.x, player.y)
        player.balance+=1000
        return True
    power_count_defender = player_atk/sector_count
    power_count_attacker = sector_def/player_count
    for i in range(len(sector.warriors)-1, -1, -1):
        if sector.warriors[i].get_power() < power_count_defender:
            del sector.warriors[i]
    for i in range(len(player.warriors)-1, -1, -1):
        if player.warriors[i].get_power()<power_count_attacker:
            del player.warriors[i]
    if len(sector.warriors)==0:
        Hip.Map.capture_sector(player.fraction, player.x, player.y)
        player.balance+=sector_def*1000
        player.fraction.owner.balance+=sector_def*500
        return True
    elif len(player.warriors)==0:
        player.x, player.y = player.fraction.getbase()
        Hip.bot.send_message(chat_id=player.user_id, text=f"Ебать, ты сдох\nВесь твой отряд кстати тоже\nТы перенесён на базу своего клана")
        return False
    else:
        return False
def get_shop(sector: Classes.Map.Sector) -> str:
    if len(sector.building.items)==0:
        return "Ничего)"
    i: Classes.Item
    text = ""
    for i in sector.building.items:
        text+=f"{i.name} - {i.cost} шекелей\n"
    return text
