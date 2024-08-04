import aiogram
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
import random

import Hip
from Hip import bot, Map, players
from Text import OnlyText
from Modules import Classes, Interface
from aiogram.filters import StateFilter

router = Router()
class Casino(aiogram.filters.state.StatesGroup):
    choose = aiogram.filters.state.State()
    bet = aiogram.filters.state.State()
@router.message(aiogram.filters.StateFilter(Casino.choose))
async def interact_enter(msg: types.Message, state=FSMContext):
    text = msg.text
    player = players[msg.from_user.id]
    kb = [
        [types.KeyboardButton(text="Поставить всё")],
        [types.KeyboardButton(text="Отмена")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    match text:
        case "Рулетка(Глобальная)":
            await state.update_data({"Choose": "Global"})
            await state.set_state(Casino.bet)
            await msg.answer("Заебок, теперь введи ставку", reply_markup=keyboard)
        case "Рулетка(В секторе)":
            await state.update_data({"Choose": "Local"})
            await state.set_state(Casino.bet)
            await msg.answer("Заебок, теперь введи ставку", reply_markup=keyboard)
        case "Камень/Ножницы/Бумага":
            await state.update_data({"Choose": "Paper"})
            await state.set_state(Casino.bet)
            await msg.answer("Заебок, теперь введи ставку", reply_markup=keyboard)
        case "Очко":
            await state.update_data({"Choose": "Ochko"})
            await state.set_state(Casino.bet)
            await msg.answer("Заебок, теперь введи ставку", reply_markup=keyboard)
        case _:
            await state.clear()
            await Interface.main_page(msg)


@router.message(aiogram.filters.StateFilter(Casino.bet))
async def casic_bet(msg: types.Message, state=FSMContext):
    choose = await state.get_state()["Choose"]
    player = players[msg.from_user.id]
    sector = Map.get_sector(player.x, player.y)
    text = msg.text
    bet = None
    if text.isdigit():
        text = int(text)
    else:
        if text=="Поставить всё":
            if player.balance>0:
                bet = player.balance
            else:
                await msg.answer("Ебаклак блять, чё ты ставить пытаешся, кого наёбываешь сучара", reply_markup=OnlyText.keyboard)
                await state.clear()
                return None
        else:
            await state.clear()
            await Interface.main_page(msg)
            return None
    match choose:
        case "Global":
            Hip.glob_room.append_user(user_id=msg.from_user.id, bet=bet)
        case "Local":
            sector.building.room.append_user(msg.from_user.id, bet=bet)
        case "Paper":
            pass
        case "Ochko":
            pass
        case _:
            await Interface.main_page(msg)
            await state.clear()