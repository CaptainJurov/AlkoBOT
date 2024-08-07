import asyncio
import time

import aiogram
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
import threading
import random
import Hip
from Hip import bot, Map, players
from Text import OnlyText
from Modules import Classes, Mechanic
from aiogram.filters import StateFilter

router = Router()
class Moving(aiogram.filters.state.StatesGroup):
    vector = aiogram.filters.state.State()
@router.message(aiogram.filters.StateFilter(Moving.vector))
async def moving_choose(msg: types.Message, state=FSMContext):
    player = players[msg.from_user.id]
    text = msg.text
    direct = (0, 0)
    if text.lower()=="вверх":
        direct = (0, -1)
    if text.lower()=="влево":
        direct = (-1, 0)
    if text.lower()=="вправо":
        direct = (1, 0)
    if text.lower()=="вниз":
        direct = (0, 1)
    if text.lower()=="отмена":
        await state.clear()
        await msg.answer("Ок", reply_markup=OnlyText.keyboard)
        return False
    sector = Map.get_sector(player.x+direct[0], player.y+direct[1])
    kd = 30 * (sector.basic_def / 2)
    if sector.building.building_type=="road":
        kd = 10 * (sector.basic_def / 2)
    player.time = int(time.time())+kd
    player.playable = False
    await msg.answer(f"Ты отправился в путь, осталось {kd} секунд")
    await state.clear()
    await asyncio.sleep(kd)
    player.playable = True
    player.move(delta_x=direct[0], delta_y=direct[1])
    sector = Map.get_sector(player.x, player.y)
    enter = f"Ты пришел в сектор [{sector.x}; {sector.y}]\nСектор принадлежит клану {sector.fraction.name}\nПостройка в секторе: {sector.building.name}"
    if not(sector.building.building_type=="void"): enter+=f"\nВладелец постройки: {sector.building.owner.name}"
    await msg.answer(enter, reply_markup=OnlyText.keyboard)
    await state.clear()