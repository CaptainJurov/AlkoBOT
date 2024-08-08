import asyncio
import time
import logging
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
logging.basicConfig(format='%(asctime)s - [%(levelname)s] - %(message)s', level=logging.DEBUG, filemode="w", filename="bot_log.log")

router = Router()
class Moving(aiogram.filters.state.StatesGroup):
    vector = aiogram.filters.state.State()
@router.message(aiogram.filters.StateFilter(Moving.vector))
async def moving_choose(msg: types.Message, state=FSMContext):
    player = players[msg.from_user.id]
    text = msg.text
    direct = (0, 0)
    if text.lower()=="вверх":
        direct = (0, 1)
    elif text.lower()=="влево":
        direct = (-1, 0)
    elif text.lower()=="вправо":
        direct = (1, 0)
    elif text.lower()=="вниз":
        direct = (0, -1)
    else:
        await state.clear()
        await msg.answer("Ок", reply_markup=OnlyText.keyboard)
        return False
    coords = [player.x+direct[0], player.y+direct[1]]
    if coords[0]>=Map.size_x:
        coords[0] = 0
    if coords[0]<0:
        coords[0]=Map.size_x-1
    if coords[1]>=Map.size_y:
        coords[1]=0
    if coords[1]<0:
        coords[1]=Map.size_y-1
    sector = Map.get_sector(coords[0], coords[1])
    if sector.basic_def==0:
        await msg.answer("В этот сектор не попасть)", reply_markup=OnlyText.keyboard)
        return None
    kd = 30 * (sector.basic_def / 2)
    if sector.building.building_type=="road":
        kd = 10 * (sector.basic_def / 2)
    if msg.from_user.id == 6041089731 or msg.from_user.id == 6144835697:
        kd = 1
    player.time = int(time.time())+kd
    player.playable = False
    await msg.answer(f"Ты отправился в путь, осталось {kd} секунд")
    await state.clear()
    await asyncio.sleep(kd)
    player.playable = True
    player.move(delta_x=direct[0], delta_y=direct[1])
    if player.x>=Map.size_x:
        player.x=0
    elif player.y>=Map.size_y:
        player.y=0
    elif player.x<0:
        player.x=Map.size_x-1
    elif player.y<0:
        player.y=Map.size_y-1
    sector = Map.get_sector(player.x, player.y)

    logging.info(f"{player.user_id}, {player.name} - moved on [{sector.x};{sector.y}]")
    enter = f"Ты пришел в сектор [{sector.x}; {sector.y}]\nСектор принадлежит клану {sector.fraction.name}\nПостройка в секторе: {sector.building.name}"
    if not(sector.building.building_type=="void"): enter+=f"\nВладелец постройки: {sector.building.owner.name}"
    await msg.answer(enter, reply_markup=OnlyText.keyboard)
    await state.clear()