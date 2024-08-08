import asyncio
import logging

import aiogram
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
import random

import Hip
from Hip import bot, Map, players
from Text import OnlyText
from Modules.Interface import main_page
from Modules import Classes
from aiogram.filters import StateFilter
logging.basicConfig(format='%(asctime)s - [%(levelname)s] - %(message)s', level=logging.DEBUG, filemode="w", filename="bot_log.log")
router = Router()
class Bank(aiogram.filters.state.StatesGroup):
    buying = aiogram.filters.state.State()
    count_buy = aiogram.filters.state.State()
    count_sell = aiogram.filters.state.State()
@router.message(aiogram.filters.StateFilter(Bank.buying))
async def choose(msg: types.Message, state=FSMContext):
    text = msg.text
    player = players[msg.from_user.id]
    coin = Hip.Coin.get_course()
    if text=="Купить гойдакоин":
        await state.set_state(Bank.count_buy)
        kb = [[
            types.KeyboardButton(text="Купить на все деньги")
        ],
        [
            types.KeyboardButton(text="Отмена")
        ]]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await msg.answer(f"Скока купишь?", reply_markup=keyboard)
    elif text=="Продать гойдакоин":
        await state.set_state(Bank.count_sell)
        kb = [[
            types.KeyboardButton(text="Продать все коины")
        ],
        [
            types.KeyboardButton(text="Отмена")
        ]]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await msg.answer("Скока продашь?", reply_markup=keyboard)
    else:
        await main_page(msg)
        await state.clear()
@router.message(aiogram.filters.StateFilter(Bank.count_buy))
async def buy(msg: types.Message, state=FSMContext):
    await state.clear()
    text = msg.text
    player = players[msg.from_user.id]
    count:int = 0
    if text.isdigit():
        count = int(text)
    else:
        if text=="Купить на все деньги":
            count = player.balance//Hip.Coin.get_course()
        else:
            await main_page(msg)
    if count<=0 or (player.balance-Hip.Coin.get_course()*count)<0:
        await msg.answer("ебаклак бедный, сьебись нахуй в места присущие нищете", reply_markup=OnlyText.keyboard)
    else:
        player.balance-=Hip.Coin.get_course()*count
        player.coins+=count
        logging.info(f"{player.user_id} {player.name} - buyed {count} coins - total cost {count*Hip.Coin.get_course()}")
        await msg.answer(f"Готово\nты купил {count} коинов на сумму {Hip.Coin.get_course()*count} шекелей\nпроверь статус", reply_markup=OnlyText.keyboard)

@router.message(aiogram.filters.StateFilter(Bank.count_sell))
async def sell(msg: types.Message, state=FSMContext):
    await state.clear()
    text = msg.text
    player = players[msg.from_user.id]
    count: int = 0
    if text.isdigit():
        count = int(text)
    else:
        if text == "Продать все коины":
            count = player.coins
        else:
            await main_page(msg)
    if count <= 0:
        await msg.answer("ебаклак бедный, сьебись нахуй в места присущие нищете", reply_markup=OnlyText.keyboard)
    elif (player.coins-count)<0:
        await msg.answer("Кого ты наебываешь сука", reply_markup=OnlyText.keyboard)
    else:
        player.balance += Hip.Coin.get_course() * count
        player.coins -= count
        logging.info(
            f"{player.user_id} {player.name} - saled {count} coins - total cost {count * Hip.Coin.get_course()}")
        await msg.answer(
            f"Готово\nты продал {count} коинов на сумму {Hip.Coin.get_course() * count} шекелей\nпроверь статус",
            reply_markup=OnlyText.keyboard)
