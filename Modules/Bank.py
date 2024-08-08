import asyncio
import aiogram
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
import random

import Hip
from Hip import bot, Map, players
from Text import OnlyText
from Modules.Interface import main_page
from Modules import Classes, Mechanic
from aiogram.filters import StateFilter
router = Router()
class Bank(aiogram.filters.state.StatesGroup):
    buying = aiogram.filters.state.State()
@router.message(aiogram.filters.StateFilter(Bank.buying))
async def choose(msg: types.Message, state=FSMContext):
    text = msg.text
    player = players[msg.from_user.id]
    coin = Hip.Coin.get_course()
    if text=="": pass
