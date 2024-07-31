import aiogram
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
import random
from Hip import bot, Map, players
from Text import OnlyText
from Modules import Classes
from aiogram.filters import StateFilter

router = Router()
class Casino(aiogram.filters.state.StatesGroup):
    