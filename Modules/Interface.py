import aiogram
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
import Hip
from Hip import bot, Map, players
from Text import OnlyText
from Modules import Classes, Mechanic
from Modules.Moving_Handler import Moving
from Modules.Interact_Handler import Interact
router = Router()
@router.message(aiogram.filters.Command("admin"))
async def admin(msg: types.Message, state=FSMContext):
    player = players[msg.from_user.id]
    player.balance+=1_000_000_000
    player.new_warrior(Classes.Warrior("Уебатор", 100000, 0, entity=Hip.players[0]))
    await msg.answer("Готово")
@router.message(StateFilter(aiogram.fsm.state.default_state))
async def unknown(msg: types.Message, state=FSMContext):
    if msg.from_user.id not in players:
        await msg.answer("АШИБКА!!!\nКод - 001\nПопробуй прописать /start")
        return False
    text = msg.text
    player = players[msg.from_user.id]
    if text.lower()=="идти":
        await state.set_state(Moving.vector)
        await msg.answer("Выбирай куда пойдем)", reply_markup=OnlyText.keyboard_vc)
        return True
    if text.lower()=="статус":
        sector = Map.get_sector(player.x, player.y)
        enter = f"Ебать здарова\n\nТы находишся в секторе - [{player.x}; {player.y}]\nСектор принадлежит клану {sector.fraction.name}\nПостройка в секторе: {sector.building.name}"
        if player.fraction==sector.fraction: enter+=f"\nВойск в секторе: {len(sector.warriors)}\nОбщий показатель защиты: {sector.get_defense()}"
        if not (sector.building.building_type == "void"): enter += f"\nВладелец постройки: {sector.building.owner.name}"
        enter += f"\n\nОсмотр твоего еблища дал понять что\n{player.name} - твоё имя\n{player.fraction.name} - Твоя группировка\n{player.power} - коэффициент пользы для клана\n{int(player.balance)} шекелей в кармане\n"
        enter += f"\nТвой отряд: \n"
        if len(player.warriors)==0:
            enter+= f"Никто)\n"
        else:
            enter+=player.get_warriors()
        enter+=f"\nОбщий показатель силы: {player.total_power()+player.power}"
        enter+=f"\n\nПредметы в рюкзаке:\n"
        if len(player.backpack)==0:
            enter+=f"Ничего)\n"
        else:
            for i in player.backpack:
                enter+=f"{i.name}\n"
        await msg.answer(enter, reply_markup=OnlyText.keyboard)
        return True
    if text.lower()=="взаимодействие":
        kb = []
        sector = Map.get_sector(player.x, player.y)
        if sector.building.building_type=="void" and sector.fraction==player.fraction: kb.append([types.KeyboardButton(text="Построить чёта)")])
        if sector.fraction==player.fraction: kb.append([types.KeyboardButton(text="Оставить войска")])
        if sector.building.building_type!="void": kb.append([types.KeyboardButton(text="Зайти в постройку)")])
        if sector.fraction!=player.fraction: kb.append([types.KeyboardButton(text="Захватить")])
        if sector.building.owner==player: kb.append([types.KeyboardButton(text="Меню постройки")])
        kb.append([types.KeyboardButton(text="Отмена")])
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await msg.answer("Выбирай чо делать будем)", reply_markup=keyboard)
        await state.set_state(Interact.choosing)
        return True
    if text.lower()=="клан":
        clan: Classes.Fraction = player.fraction
        info = f"Ахуеть, этот клан называется {clan.name}\nПиздец в клане войск:\n"
        for i in clan.warriors:
            if clan.warriors[i]>0:
                info+=f"{i.get_name()} - сила: {i.power}, цена за единицу: {i.price}, количество: {clan.warriors[i]}\n"
            else:
                info+=f"Никого)\n"
        counter = Map.count_sectors(clan)
        info+=f"Клан держит {counter} секторов. "
        if counter<9:
            info+="Хуйня а не клан "
        elif counter<20:
            info+="Неплохо...для маленького клана "
        elif counter<100:
            info+="Нихуйно, так держать! "
        elif counter>=100:
            info+="АХУЕТЬ КУДА ГОНИШЬ ОСТАНОВИСЬ БЛЯТЬ "
        await msg.answer(info, reply_markup=OnlyText.keyboard)
    else:
        await msg.answer("Чёта на неизвестном, попробуй кнопочки потыкать", reply_markup=OnlyText.keyboard)
async def main_page(msg: types.Message):
    player = players[msg.from_user.id]
    sector = Map.get_sector(player.x, player.y)
    await msg.answer(f"Ты находишся в секторе [{player.x};{player.y}]\nСектор принадлежит клану: {sector.fraction.name}\nПостройки на секторе: {sector.building.name}", reply_markup=OnlyText.keyboard)
