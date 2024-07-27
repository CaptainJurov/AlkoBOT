#Переход на новую строку [ \n ]
import aiogram
main_kb = [[
    aiogram.types.KeyboardButton(text="Идти"),
aiogram.types.KeyboardButton(text="Взаимодействие"),
],
[aiogram.types.KeyboardButton(text="Статус"),aiogram.types.KeyboardButton(text="Клан"),]]
keyboard = aiogram.types.ReplyKeyboardMarkup(keyboard=main_kb, resize_keyboard=True)

vector_kb = [[aiogram.types.KeyboardButton(text="Вверх")], [aiogram.types.KeyboardButton(text="Влево"), aiogram.types.KeyboardButton(text="Отмена"),aiogram.types.KeyboardButton(text="Вправо")], [aiogram.types.KeyboardButton(text="Вниз")]]
keyboard_vc = aiogram.types.ReplyKeyboardMarkup(keyboard=vector_kb, resize_keyboard=True)


start_message = "Ебать здарова чё каво\nЭтот бот является симулятором политики и игрушкой наблюдателя а.к.а админа\nЕсли возникает ошибка или баг не стесняйся писать на @frogget282"
