import aiogram
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
import Hip
import config
from Hip import bot, Map, players, Interact
from Text import OnlyText
from Modules import Classes, Mechanic
from Modules.Moving_Handler import Moving
import logging

router = Router()
async def change_user_state(user_id: int, new_state):
    # Получаем контекст состояния для пользователя
    async with FSMContext(Hip.storage, config.keys) as state:
        user = await state.get_user(user_id)
        await state.set_state(state=new_state)
class ChooseClan(aiogram.filters.state.StatesGroup):
    choosing = aiogram.filters.state.State()
    nickname = aiogram.filters.state.State()
    clan_page = aiogram.filters.state.State()
    create_clan = aiogram.filters.state.State()
    settings = aiogram.filters.state.State()
    warriors_id = aiogram.filters.state.State()
    warrior_name = aiogram.filters.state.State()
    kick = aiogram.filters.state.State()
    kicked = aiogram.filters.state.State()
    ban = aiogram.filters.state.State()
    unban = aiogram.filters.state.State()
@router.message(aiogram.filters.Command("admin"))
async def admin(msg: types.Message, state=FSMContext):
    player = players[msg.from_user.id]
    logging.info(f"{player.user_id}, {player.name} - typed ADMIN")
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
    match text.lower():
        case "идти":
            await state.set_state(Moving.vector)
            await msg.answer("Выбирай куда пойдем)", reply_markup=OnlyText.keyboard_vc)
            return True
        case "статус":
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
        case "взаимодействие":
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
        case "клан":
            await state.set_state(ChooseClan.clan_page)
            kb = []
            if player.fraction.owner!=player:
                kb.append([types.KeyboardButton(text="Создать свой клан[1млрд шек.]")])
            if player==player.fraction.owner:
                kb.append([types.KeyboardButton(text="Управление")])
            kb.append( [types.KeyboardButton(text="Ничего")])
            clan: Classes.Fraction = player.fraction
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
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
            info+=f"\n\nнабор новичков {"открыт" if player.fraction.open else "закрыт"}"
            await msg.answer(info, reply_markup=keyboard)
        case "выебать ослика":
            await msg.answer("Под хлюпающие звуки и томное дыхание копытного, ты злачно кончил в ишака", reply_markup=OnlyText.keyboard)
        case _:
            await msg.answer("Чёта на неизвестном, попробуй кнопочки потыкать", reply_markup=OnlyText.keyboard)
async def main_page(msg: types.Message):
    player = players[msg.from_user.id]
    sector = Map.get_sector(player.x, player.y)
    await msg.answer(f"Ты находишся в секторе [{player.x};{player.y}]\nСектор принадлежит клану: {sector.fraction.name}\nПостройки на секторе: {sector.building.name}", reply_markup=OnlyText.keyboard)
