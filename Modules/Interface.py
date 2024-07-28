import aiogram
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

import Hip
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
    enter = aiogram.filters.state.State()
    build = aiogram.filters.state.State()
    work = aiogram.filters.state.State()
class Buildings(aiogram.filters.state.StatesGroup):
    working = aiogram.filters.state.State()
    choosing = aiogram.filters.state.State()
    shop_choosing = aiogram.filters.state.State()
    settings = aiogram.filters.state.State()
    settings_rename = aiogram.filters.state.State()
    settings_accept = aiogram.filters.state.State()
@router.message(aiogram.filters.Command("admin"))
async def admin(msg: types.Message, state=FSMContext):
    player = players[msg.from_user.id]
    player.balance+=1_000_000_000
    await msg.answer("Готово")
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
async def moving_choose(msg: types.Message, state=FSMContext):
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
@router.message(aiogram.filters.StateFilter(Interact.choosing))
async def inter_choose(msg: types.Message, state=FSMContext):
    text = msg.text.lower()
    player = players[msg.from_user.id]
    sector = Map.get_sector(player.x, player.y)
    if text=="зайти в постройку)":
        await state.set_state(Interact.enter)
        kb = OnlyText.main_kb
        building_type = sector.building.building_type
        if building_type=="spawn" or building_type=="void":
            await state.clear()
        if building_type=="shop" or building_type=="tavern" or building_type=="casino" or building_type=="bank":
            await msg.answer("coming soon")
            await state.clear()
            return False
        if building_type=="work":
            kb = [[types.KeyboardButton(text="Работать")], [types.KeyboardButton(text="Сьебаться в страхе")]]

        await msg.answer(f"Ты зашел в {sector.building.name}\nВладелец: {sector.building.owner.name}\n", reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))
    if text=="построить чёта)":
        await state.set_state(Interact.build)
        kb = []
        for i in Hip.buildings:
            kb.append([types.KeyboardButton(text=i)])
        kb.append([types.KeyboardButton(text="Отмена")])
        keyboard=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await msg.answer( f"кароч, ты можешь тут построить следующие постройки:\n{Hip.get_all()}", reply_markup=keyboard)
    if text=="захватить":
        await state.clear()
        if player.power>sector.get_defense():
            defense = sector.get_defense()
            reward = defense*10000
            losses = player.power*(defense/player.power)
            player.balance+=reward
            Map.capture_sector(player.fraction, player.x, player.y)
            await msg.answer(f"Нихуйно, сектор захвачен\nТвоя награда: {reward:,} шекелей\nГлава клана будет уведомлён о твоих достижениях")
            try:
                await bot.send_message(chat_id=player.fraction.owner.id, text=f"Игрок {player.name} захватил сектор [{sector.x};{sector.y}]\nЗащита сектора при атаке: {defense}\nПоказатель атаки игрока: {player.power}")
            except:
                print("sector has been captured")

        else:
            await msg.answer("Ебать ты слабость, не вывез\n\nПоказатель полезности для клана сброшен\nТы сдох", reply_markup=OnlyText.keyboard)
            player.x, player.y = player.fraction.getbase()
            player.power = 1
            _, losses = Mechanic.calculate_losses(player.power, sector.get_defense(), sector.basic_def)

    if text=="меню постройки":
        await state.set_state(Buildings.settings)
        kb=[[types.KeyboardButton(text="Переименовать")], [types.KeyboardButton(text="Продать к хуям")]]
        keyboard=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await msg.answer(f"Здарова начальник\nИмя постройки - {sector.building.name}\nТип постройки - {sector.building.firstname}", reply_markup=keyboard)
@router.message(aiogram.filters.StateFilter(Buildings.settings))
async def building_settings(msg: types.Message, state=FSMContext):
    text = msg.text
    if text=="Переименовать":
        await state.set_state(Buildings.settings_rename)
        await msg.answer("Введи новое название постройки(Максимум 50 символов)", reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="Отмена")]], resize_keyboard=True))
        return True
    if text=="Продать к хуям":
        await state.set_state(Buildings.settings_accept)
        await msg.answer("Ты точно хочешь это сделать?\nТебе вернется 80% стоимости", reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="Нет")], [types.KeyboardButton(text="Продать к хуям")]], resize_keyboard=True))
        return True
    await state.clear()
    await msg.answer("Ты вышел из здания", reply_markup=OnlyText.keyboard)
@router.message(aiogram.filters.StateFilter(Buildings.settings_rename))
async def building_settings_rename(msg: types.Message, state=FSMContext):
    text = msg.text
    player = players[msg.from_user.id]
    sector = Map.get_sector(player.x, player.y)
    if text=="Отмена":
        await state.clear()
        await msg.answer("Ок", reply_markup=OnlyText.keyboard)
        return False
    if len(text)>50:
        await state.clear()
        await msg.answer("алё блять по русски написано 50 символов максимум", reply_markup=True)
        return False
    sector.building.name = text
    await state.clear()
    await msg.answer("Постройка переименована, надеюсь оно того стоило", reply_markup=OnlyText.keyboard)
@router.message(aiogram.filters.StateFilter(Buildings.settings_accept))
async def building_settings_delete(msg: types.Message, state=FSMContext):
    text = msg.text
    player = players[msg.from_user.id]
    sector = Map.get_sector(player.x, player.y)
    if text=="Продать к хуям":

        cost=(Hip.buildings_for_types[sector.building.building_type].price)*0.8
        player.balance+=cost
        sector.destroy()
        await msg.answer(f"Тебе хватило смелости продать постройку\nКошелек пополнен на {cost:,} шекелей", reply_markup=OnlyText.keyboard)
    else:

        await msg.answer("Рад за тебя", reply_markup=OnlyText.keyboard)
    await state.clear()
@router.message(aiogram.filters.StateFilter(Interact.enter))
async def interact_enter(msg: types.Message, state=FSMContext):
    text = msg.text.lower()
    player = players[msg.from_user.id]
    sector = Map.get_sector(player.x, player.y)
    if sector.building.building_type=="work":
        if text=="работать":
            await msg.answer("Всё ахуенно, ты батрачишь")
            await state.set_state(Buildings.working)
        if text=="сьебаться в страхе":
            await state.clear()
            await msg.answer("Ссыкло ебливое убежал к мамочке плакаться на могилку", reply_markup=OnlyText.keyboard)
@router.message(aiogram.filters.StateFilter(Interact.build))
async def interact_building(msg: types.Message, state=FSMContext):
    text = msg.text
    player = players[msg.from_user.id]
    sector = Map.get_sector(player.x, player.y)
    sp = []
    for j in Hip.buildings:
        sp.append(j)
    if not(text in sp):
        await msg.answer("АШИБКА КОД 002\nЖми на кнопки еблан", reply_markup=OnlyText.keyboard)
        await state.clear()
        return False
    building: Hip.Building = Hip.buildings[text]
    if player.balance>=building.price:
        if sector.building.building_type=="void":
            sector.build(Map.Sector.Building(building.name, player, building_type=building.type))
            player.balance-=building.price

            await msg.answer(f"Заебок\nЗдание {building.name} успешно построено\nпереименовать постройку можно в меню взаимодействия", reply_markup=OnlyText.keyboard)
        else:
            await msg.answer("АШИБКА КОД 003\nНа секторе уже чёта есть", reply_markup=OnlyText.keyboard)

    else:
        await msg.answer("Хуйня нищая, накопи столько сначала", reply_markup=OnlyText.keyboard)
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
        if sector.building.building_type=="void": kb.append([types.KeyboardButton(text="Построить чёта)")])
        else: kb.append([types.KeyboardButton(text="Зайти в постройку)")])
        if sector.fraction!=player.fraction: kb.append([types.KeyboardButton(text="Захватить")])
        if sector.building.owner==player: kb.append([types.KeyboardButton(text="Меню постройки")])
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
    else:
        await msg.answer("Чёта на неизвестном, попробуй кнопочки потыкать", reply_markup=OnlyText.keyboard)


