import aiogram
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
import random
import Hip
from Hip import bot, Map, players
from Text import OnlyText
from Modules import Classes, Mechanic
from aiogram.filters import StateFilter


router = Router()


class Buildings(aiogram.filters.state.StatesGroup):
    working = aiogram.filters.state.State()
    choosing = aiogram.filters.state.State()
    shop_choosing = aiogram.filters.state.State()
    settings = aiogram.filters.state.State()
    settings_rename = aiogram.filters.state.State()
    settings_accept = aiogram.filters.state.State()


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
