import aiogram
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
import random
import Hip
from Hip import bot, Map, players
from Text import OnlyText
from Modules import Classes
from Modules.Interface import ChooseClan, main_page
from aiogram.filters import StateFilter

router = Router()


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
        if choose in range(1, len(Map.fraction_list)) and choose!=0 and Map.fraction_list[choose].open:
            user_id = msg.from_user.id
            frac = Map.fraction_list[choose]
            players[user_id] = Classes.Player(user_id, frac, nickname=str(user_id))
            print("new player", user_id, msg.from_user.username)
            await msg.answer(f"Ахуительно, теперь ты с братвой клана [{frac.name}]\nКоординаты спавна фракции - [x={frac.x}; y={frac.y}]")
            await msg.answer(f"Теперь самое вкусное)\nВведи своё погоняло")
            await state.set_state(ChooseClan.nickname)
            return True
        if not(Map.fraction_list[choose].open):
            await msg.answer("Данная фракция закрыла набор новичков")
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
@router.message(aiogram.filters.StateFilter(ChooseClan.clan_page))
async def page(msg: types.Message, state=FSMContext):
    if msg.text=="Создать свой клан[1млрд шек.]":
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
        ]]
        await msg.answer()
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
                    player.fraction = frac
                    await state.clear()
                    await msg.answer("Ух ты ж нихуя себе, поздравляю, дорогой, ты создал аж свою фракцию, скорее захватывай всё в округе и будь готов к защите", reply_markup=OnlyText.keyboard)
                else:
                    await state.clear()
                    await msg.answer("я не ебу как ты умудрился деньги проебать, но сейчас тебе не хватает на создание клана", reply_markup=OnlyText.keyboard)
                    return None
    else:
        await msg.answer("Пока ты выбирал название, в секторе появились войска", reply_markup=OnlyText.keyboard)
        await state.clear()
