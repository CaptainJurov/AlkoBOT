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
casic_rejim = """
Рулетка - Побеждает богатейший, твои шансы на победу равняются твоей ставке, но не забывай что это лишь 'шанс'
Есть 2 вида рулетки
Глобальная - Тут сидят самые ебнутые лудоманы со всего бота, привязки к месту нет
Локальная - Твои соперники находятся там же где и ты, привязка к месту

Камень/Ножницы/Бумага - Мне обязательно писать о том как это работает? Игра локальная, в секторе

Очко - игра с ботом, о том как это работает загугли, мне лень писать
"""