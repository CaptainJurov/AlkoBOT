import aiogram
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from Hip import bot, Map, players
from Text import OnlyText
from Modules import Classes
from aiogram.filters import StateFilter

router = Router()
class ChooseClan(aiogram.filters.state.StatesGroup):
    choosing = aiogram.filters.state.State()
    nickname = aiogram.filters.state.State()
class Moving(aiogram.filters.state.StatesGroup):
    vector = aiogram.filters.state.State()
class Interact(aiogram.filters.state.StatesGroup):
    interact = aiogram.filters.state.State()
    choosing = aiogram.filters.state.State()
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
        if choose in range(1, len(Map.fraction_list)) and choose!=0:
            user_id = msg.from_user.id
            frac = Map.fraction_list[choose]
            players[user_id] = Classes.Player(user_id, frac, nickname=str(user_id))
            print("new player", user_id, msg.from_user.username)
            await msg.answer(f"Ахуительно, теперь ты с братвой клана [{frac.name}]\nКоординаты спавна фракции - [x={frac.x}; y={frac.y}]")
            await msg.answer(f"Теперь самое вкусное)\nВведи своё погоняло")
            await state.set_state(ChooseClan.nickname)
            return True
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
    await msg.answer("Ахуительно, теперь ты готов к адской дрочильне", reply_markup=OnlyText.keyboard)
    await state.clear()
@router.message(aiogram.filters.StateFilter(Moving.vector))
async def Moving_choose(msg: types.Message, state=FSMContext):
    player = players[msg.from_user.id]
    text = msg.text
    if text.lower()=="вверх":
        player.move(0, -1)
    if text.lower()=="влево":
        player.move(-1, 0)
    if text.lower()=="вправо":
        player.move(1, 0)
    if text.lower()=="вниз":
        player.move(0, 1)
    if text.lower()=="отмена":
        await state.clear()
        await msg.answer("Ок", reply_markup=OnlyText.keyboard)
        return False

    sector = Map.get_sector(player.x, player.y)
    enter = f"Ты пришел в сектор [{sector.x}; {sector.y}]\nСектор принадлежит клану {sector.fraction.name}\nПостройка в секторе: {sector.building.name}"
    if not(sector.building.building_type=="void"): enter+=f"\nВладелец постройки: {sector.building.owner.name}"
    await msg.answer(enter, reply_markup=OnlyText.keyboard)
    await state.clear()

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
        if not (sector.building.building_type == "void"): enter += f"\nВладелец постройки: {sector.building.owner.name}"
        enter += f"\n\nОсмотр твоего еблища дал понять что\n{player.name} - твоё имя\n{player.fraction.name} - Твоя группировка\n{player.power} - коэффициент пользы для клана\n{player.balance} шекелей в кармане"
        await msg.answer(enter, reply_markup=OnlyText.keyboard)
        return True
    if text.lower()=="взаимодействие":
        await state.set_state(Interact.interact)
        kb = []
        sector = Map.get_sector(player.x, player.y)
        if sector.building.building_type=="void": kb.append(types.KeyboardButton(text="Построить чёта)"))
        else: kb.append(types.KeyboardButton(text="Зайти в постройку)"))
        if sector.fraction!=player.fraction: kb.append(types.KeyboardButton(text="Захватить"))
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


