import aiogram
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
import random
import Hip
from Hip import bot, Map, players
from Text import OnlyText
from Modules import Classes
from Modules.Interface import ChooseClan, main_page, change_user_state
from aiogram.filters import StateFilter
from aiogram.filters.base import Filter
import logging
logging.basicConfig(format='%(asctime)s - [%(levelname)s] - %(message)s', level=logging.DEBUG, filemode="w", filename="bot_log.log")

router = Router()
class CustomFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id in Hip.kicked
@router.message(CustomFilter())
async def filter(msg: types.Message, state=FSMContext):
    await state.set_state(ChooseClan.kicked)
    Hip.kicked.remove(msg.from_user.id)
    text = f"Тебя кикнули с клана\n\nСписок доступных фракций:\n"
    kb = []
    for i in range(1, len(Map.fraction_list)):
        text += f"[{i}] - {Map.fraction_list[i].name}\n"
        kb.append([types.KeyboardButton(text=str(i))])
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
    await msg.answer(text, reply_markup=keyboard)
@router.message(aiogram.filters.StateFilter(ChooseClan.kicked))
async def kicked(msg: types.Message, state=FSMContext):
    player = players[msg.from_user.id]
    text_t = msg.text
    try:
        choose = int(msg.text)
        if choose in range(1, len(Map.fraction_list)) and choose != 0 and Map.fraction_list[choose].open and \
                Map.fraction_list[choose].check_user(user_id=msg.from_user.id):
            user_id = msg.from_user.id
            frac = Map.fraction_list[choose]
            player.fraction = frac
            frac.players.append(players[user_id])
            await msg.answer(
                f"Ахуительно, теперь ты с братвой клана [{frac.name}]\nКоординаты спавна фракции - [x={frac.x}; y={frac.y}]")
            return True
        if not (Map.fraction_list[choose].open):
            await msg.answer("Данная фракция закрыла набор новичков")
            return None
        if not (Map.fraction_list[choose].check_user(user_id=msg.from_user.id)):
            await msg.answer("Тебя ебаклака забанили в этом клане, выбирай другой")
            return None
        await msg.answer(f"Умный дохуя?")
    except:

        text = "Список доступных фракций:\n"
        kb = []
        for i in range(1, len(Map.fraction_list)):
            text += f"[{i}] - {Map.fraction_list[i].name}\n"
            kb.append([types.KeyboardButton(text=str(i))])
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
        await msg.answer(text, reply_markup=keyboard)
@router.message(aiogram.filters.Command("start"))
async def unknown(msg: types.Message, state=FSMContext):
    user_id = msg.from_user.id
    if user_id not in players:
        await state.set_state(ChooseClan.choosing)
        await msg.answer(OnlyText.start_message)
        text = "Список доступных фракций:\n"
        kb = []
        for i in range(1, len(Map.fraction_list)):
            text+=f"[{i}] - {Map.fraction_list[i].name}\n"
            kb.append([types.KeyboardButton(text=str(i))])
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
        await msg.answer(text, reply_markup=keyboard)
    else:
        await msg.answer("Всё заебок ты в игре")
@router.message(aiogram.filters.StateFilter(ChooseClan.choosing))
async def choosing(msg: types.Message, state=FSMContext):
    try:
        choose = int(msg.text)
        if choose in range(1, len(Map.fraction_list)) and choose!=0 and Map.fraction_list[choose].open and Map.fraction_list[choose].check_user(user_id=msg.from_user.id):
            user_id = msg.from_user.id
            frac = Map.fraction_list[choose]
            players[user_id] = Classes.Player(user_id, frac, nickname=str(user_id))
            frac.players.append(players[user_id])
            print("new player", user_id, msg.from_user.username)
            await msg.answer(f"Ахуительно, теперь ты с братвой клана [{frac.name}]\nКоординаты спавна фракции - [x={frac.x}; y={frac.y}]")
            await msg.answer(f"Теперь самое вкусное)\nВведи своё погоняло")
            await state.set_state(ChooseClan.nickname)
            return True
        if not(Map.fraction_list[choose].open):
            await msg.answer("Данная фракция закрыла набор новичков")
        if not(Map.fraction_list[choose].check_user(user_id=msg.from_user.id)):
            await msg.answer("Тебя ебаклака забанили в этом клане, выбирай другой")
        await msg.answer(f"Умный дохуя?")
    except:
        await msg.answer("Долбаеб блять жми кнопки и выбирай по человечески")

@router.message(aiogram.filters.StateFilter(ChooseClan.nickname))
async def choosing_nickname(msg: types.Message, state=FSMContext):
    text = msg.text
    if len(text)>30:
        await msg.answer("Ебанат, сказано никнейм написать, а не Войну и Мир переписывать\n(30 символов край брат)")
        return False
    player = players[msg.from_user.id]
    player.name = text
    logging.info(f"{player.user_id}, {player.name} - choosed clan {player.fraction.name}")
    await msg.answer("Ахуительно, теперь ты готов к адской дрочильне", reply_markup=OnlyText.keyboard)
    await state.clear()
@router.message(aiogram.filters.StateFilter(ChooseClan.clan_page))
async def page(msg: types.Message, state=FSMContext):
    if msg.text=="Создать свой клан[1 лям шек.]":
        player = players[msg.from_user.id]
        if player.balance>=1_000_000_000:
            sector = Map.get_sector(player.x, player.y)
            if len(sector.warriors)==0:
                await state.set_state(ChooseClan.create_clan)
                await msg.answer("Всё заебись, введи название будущего клана(50 символов максимум)", reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="Отмена")]], resize_keyboard=True))
            else:
                await state.clear()
                await msg.answer("Так то всё в порядке, денег хватает\nВот только ты сейчас в секторе, в котором есть войска, найди пустой сектор либо захвати вражеский", reply_markup=OnlyText.keyboard)
        else:
            await state.clear()
            await msg.answer("Хуйня нищая, тебе еще копить и копить до своей фракции", reply_markup=OnlyText.keyboard)
    elif msg.text=="Управление":
        await state.set_state(ChooseClan.settings)
        kb = [[
            types.KeyboardButton(text="Переименовать войска"),
        ],
        [
            types.KeyboardButton(text="Закрыть/Открыть клан")
        ],
        [
            types.KeyboardButton(text="Кикнуть чела")
        ],
        [
            types.KeyboardButton(text="Забанить чела")
        ],
        [
            types.KeyboardButton(text="Разбанить чела")
        ],
        [
            types.KeyboardButton(text="Отмена")
        ]]
        await msg.answer("Выбирай чё делать будем", reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))
    else:
        await state.clear()
        await main_page(msg)
@router.message(aiogram.filters.StateFilter(ChooseClan.create_clan))
async def page_create(msg: types.Message, state=FSMContext):
    player = players[msg.from_user.id]
    sector = Map.get_sector(player.x, player.y)
    if len(sector.warriors)==0:
        if msg.text=="Отмена":
            await state.clear()
            await msg.answer("Дело твоё", reply_markup=OnlyText.keyboard)
            return None
        else:
            if len(msg.text)>50:
                await state.clear()
                await msg.answer("Еблаход, по русски написано 50 символов блять", reply_markup=OnlyText.keyboard)
                return None
            else:
                if player.balance>=1_000_000_000:
                    player.balance -= 1_000_000_000
                    frac = Map.create_clan(Classes.Fraction(msg.text, player.x, player.y, player=player))
                    player.fraction.kick_man(player)
                    player.fraction = frac
                    logging.info(f"{player.user_id}, {player.name} - created clan {frac.name}")
                    await state.clear()
                    await msg.answer("Ух ты ж нихуя себе, поздравляю, дорогой, ты создал аж свою фракцию, скорее захватывай всё в округе и будь готов к защите", reply_markup=OnlyText.keyboard)
                else:
                    await state.clear()
                    await msg.answer("я не ебу как ты умудрился деньги проебать, но сейчас тебе не хватает на создание клана", reply_markup=OnlyText.keyboard)
                    return None
    else:
        await msg.answer("Пока ты выбирал название, в секторе появились войска", reply_markup=OnlyText.keyboard)
        await state.clear()
@router.message(aiogram.filters.StateFilter(ChooseClan.settings))
async def page_settings(msg: types.Message, state=FSMContext):
    player = players[msg.from_user.id]
    text = msg.text
    if text=="Переименовать войска":
        await state.set_state(ChooseClan.warriors_id)
        text_to_send = ""
        kb = []
        for i in range(len(player.fraction.warriors_types)):
            text_to_send+=f"\n[{i+1}] - {player.fraction.warriors_types[i].get_name()}"
            kb.append([types.KeyboardButton(text=f"{i+1}")])
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await msg.answer(text_to_send, reply_markup=keyboard)
    elif text=="Закрыть/Открыть клан":
        player.fraction.open = not(player.fraction.open)
        await msg.answer("Готово", reply_markup=OnlyText.keyboard)
        await state.clear()
    elif text=="Кикнуть чела":
        await state.set_state(ChooseClan.kick)
        await msg.answer(f"\nВведи id или игровой ник игрока)\n@id <- эта хуйня не сработает, чтобы получить id человека надо в тг включить режим разработчика", reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="Отмена")]], resize_keyboard=True))
    elif text=="Забанить чела":
        await state.set_state(ChooseClan.ban)
        await msg.answer("Пиши id или игровой ник игра чтобы забанить\n@id <- эта хуйня не сработает, чтобы получить id человека надо в тг включить режим разработчика", reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="Отмена")]], resize_keyboard=True))
    elif text=="Разбанить чела":
        await state.set_state(ChooseClan.unban)
        await msg.answer(
            "Пиши id или игровой ник игра чтобы разбанить\n@id <- эта хуйня не сработает, чтобы получить id человека надо в тг включить режим разработчика",
            reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="Отмена")]],
                                                   resize_keyboard=True))
    else:
        await main_page(msg)
        await state.clear()
@router.message(aiogram.filters.StateFilter(ChooseClan.ban))
async def banning(msg: types.Message, state=FSMContext):
    text = msg.text
    player = players[msg.from_user.id]
    i: Classes.Player
    for i in player.fraction.players:
        if i.user_id == text or i.name == text:
            logging.info(f"{player.user_id}, {player.name} - banned from clan {player.fraction.name} user {i.name} {i.user_id} ")
            player.fraction.kick_man(i)
            Hip.kicked.append(i.user_id)
            await bot.send_message(chat_id=i.user_id, text="Тебя забанили к хуям в клане, выбирай новый")
            await msg.answer("Долбаёб успешно получил по еблу", reply_markup=OnlyText.keyboard)
            player.fraction.banned_players[str(i.user_id)] = i
            await state.clear()
            return True
    await msg.answer("Чел не найден...\nвведи заново", reply_markup=OnlyText.keyboard)
    await state.clear()
@router.message(aiogram.filters.StateFilter(ChooseClan.unban))
async def unbanning(msg: types.Message, state=FSMContext):
    player = players[msg.from_user.id]
    text = msg.text
    unbanned = text
    for i in player.fraction.banned_players:
                    if player.fraction.banned_players[i].name==text:
                        unbanned = i
                        logging.info(f"{player.user_id}, {player.name} - unban from clan {player.fraction.name} user {i.name} {i.user_id}")
                        await msg.answer("Чел разбанен", reply_markup=OnlyText.keyboard)
                        await state.clear()
                        player.fraction.unban(unbanned)
                        return None
    await msg.answer("Чел не найден в списках забаненных", reply_markup=OnlyText.keyboard)
    await state.clear()
@router.message(aiogram.filters.StateFilter(ChooseClan.warriors_id))
async def warrior_id(msg: types.Message, state=FSMContext):
    player = players[msg.from_user.id]
    text = msg.text
    if text=="Отмена":
        await main_page(msg)
        await state.clear()
    try:
        text = int(text)
        warrior = player.fraction.warriors_types[text-1]
        Hip.storaga[msg.from_user.id] = warrior
        await msg.answer("Введи новое наименование вояки", reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="Отмена")]], resize_keyboard=True))
        await state.set_state(ChooseClan.warrior_name)
    except:
        await msg.answer("Чо", reply_markup=OnlyText.keyboard)
@router.message(aiogram.filters.StateFilter(ChooseClan.warrior_name))
async def warrior_name(msg: types.Message, state=FSMContext):
    player = players[msg.from_user.id]
    warrior = Hip.storaga[msg.from_user.id]
    if msg.text=="Отмена":
        await main_page(msg)
        await state.clear()
    if len(msg.text)<50:
        logging.info(f"{player.user_id}, {player.name} - renamed warrior {warrior.name} on {msg.text} in clan {player.fraction.name}")
        warrior.name = msg.text
        await msg.answer("Готово", reply_markup=OnlyText.keyboard)
        await state.clear()
    else:
        await msg.answer("Долбаёб блять, 50 символов максимум")
@router.message(aiogram.filters.StateFilter(ChooseClan.kick))
async def clan_kick(msg: types.Message, state=FSMContext):
    text = msg.text
    player = players[msg.from_user.id]
    i: Classes.Player
    for i in player.fraction.players:
            if i.user_id==text or i.name==text:
                player.fraction.kick_man(i)
                logging.info(f"{player.user_id}, {player.name} - kicked from clan {player.fraction.name} user {i.name} {i.user_id}")
                Hip.kicked.append(i.user_id)
                await bot.send_message(chat_id=i.user_id, text="Тебя кикнули к хуям с клана, выбирай новый")
                await msg.answer("Долбаёб успешно получил по еблу", reply_markup=OnlyText.keyboard)
                await state.clear()
                return True
    await msg.answer("Чел не найден...\nвведи заново", reply_markup=OnlyText.keyboard)
    await state.clear()
