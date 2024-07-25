import aiogram
from aiogram import types, Router, F
from Hip import bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import StateFilter
router = Router()
@router.message(StateFilter(aiogram.fsm.state.default_state))
async def unknown(msg: types.Message):
    await msg.answer("Чёта на неизвестном)")