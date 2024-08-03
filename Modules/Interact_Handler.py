import aiogram
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
import random
import Hip
from Hip import bot, Map, players, Interact
from Text import OnlyText
from Modules.Building_Handler import Buildings
from Modules.Casino import Casino
from Modules.Interface import main_page
from Modules import Classes, Mechanic
from aiogram.filters import StateFilter

router = Router()

@router.message(aiogram.filters.StateFilter(Interact.warriors))
async def inter_choose_warriors(msg: types.Message, state=FSMContext):
    player = players[msg.from_user.id]
    sector = Map.get_sector(player.x, player.y)
    text = msg.text
    if text=="Отмена":
        await state.clear()
        await main_page()
        return False
    warrior = player.warriors
    founded = False
    i: Classes.Warrior
    for i in range(len(warrior)):
        if text == player.warriors[i].name:
            player.balance += player.warriors[i].price
            sector.new_warrior(player.warriors.pop(i))
            founded=True
            break
    if not founded:
        await msg.answer("Солдат не найден(Отряд не заметил потери бойца)", reply_markup=OnlyText.keyboard)
        await state.clear()
    else:
        await msg.answer("Родина-клан гордится вами\nБаланс пополнен", reply_markup=OnlyText.keyboard)
        await state.clear()


@router.message(aiogram.filters.StateFilter(Interact.choosing))
async def inter_choose(msg: types.Message, state=FSMContext):
    text = msg.text.lower()
    player = players[msg.from_user.id]
    sector = Map.get_sector(player.x, player.y)
    if text=="отмена":
        await state.clear()
        await main_page(msg)

    if text=="оставить войска":
        await state.set_state(Interact.warriors)
        kb = []
        i: Classes.Warrior
        text_to_send = ""
        if len(player.warriors)==0:
            text_to_send+=f"Никто))\n"
        else:
            for i in player.warriors:
                kb.append([types.KeyboardButton(text=f"{i.name}")])
                text_to_send += f"\n{i.get_name()} - сила: {i.power}; цена - {i.price}"
        kb.append([types.KeyboardButton(text="Отмена")])
        await msg.answer(f"Выбирай кого оставишь тут\n{text_to_send}", reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))
    if text=="зайти в постройку)":
        await state.set_state(Interact.enter)
        kb = OnlyText.main_kb
        building_type = sector.building.building_type
        try:
            vladelec=sector.building.owner.name
        except:
            vladelec = "Server"
        text_to_send = f"Ты зашел в {sector.building.name}\nВладелец: {vladelec}\n"
        if building_type=="spawn" or building_type=="void" or building_type=="road":
            await state.clear()
        if building_type=="shop":
            kb = []
            for i in sector.building.items:
                kb.append([types.KeyboardButton(text=f"{i.name}")])
            text_to_send+=f"Ассортимент:\n{Mechanic.get_shop(sector)}"
            #kb = [[types.KeyboardButton(text=)]]
        if building_type=="tavern" or building_type=="casino" or building_type=="bank":
            await msg.answer("coming soon")
            await state.clear()
            return False
        if building_type=="work":
            kb = [[types.KeyboardButton(text="Работать")], [types.KeyboardButton(text="Сьебаться в страхе")]]
        if building_type=="warriors":
            kb = []
            i: Classes.Warrior
            for i in player.fraction.warriors_types:
                kb.append([types.KeyboardButton(text=f"{i.name}")])
                text_to_send+=f"\n{i.get_name()} - сила: {i.power}; цена - {i.price}"

        if kb!=OnlyText.keyboard: kb.append([types.KeyboardButton(text="Отмена")])
        await msg.answer(text_to_send, reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))
    if text=="построить чёта)":
        await state.set_state(Interact.build)
        kb = []
        for i in Hip.buildings:
            kb.append([types.KeyboardButton(text=i)])
        kb.append([types.KeyboardButton(text="Отмена")])
        keyboard=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await msg.answer( f"кароч, ты можешь тут построить следующие постройки:\n{Hip.get_all()}", reply_markup=keyboard)
    if text=="захватить":
        await state.set_state(Interact.capture)
        kb = [[types.KeyboardButton(text="Атаковать")], [types.KeyboardButton(text="Сьебаться обоссавшись")]]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await msg.answer(f"Смелое решение\nВ этом секторе сидят {len(sector.warriors)} вояк\nВсё еще хочешь этот сектор?", reply_markup=keyboard)

    if text=="меню постройки" and player==player.fraction.owner:
        await state.set_state(Buildings.settings)
        kb=[[types.KeyboardButton(text="Переименовать")], [types.KeyboardButton(text="Продать к хуям")]]
        keyboard=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await msg.answer(f"Здарова начальник\nИмя постройки - {sector.building.name}\nТип постройки - {sector.building.firstname}", reply_markup=keyboard)

@router.message(aiogram.filters.StateFilter(Interact.capture))
async def capturing(msg: types.Message, state=FSMContext):
    player = players[msg.from_user.id]
    sector = Map.get_sector(player.x, player.y)
    sector_len = len(sector.warriors)
    sector_frac = sector.fraction
    await state.clear()
    if msg.text!="Атаковать":
        await msg.answer("Ссыкло ебливое", reply_markup=OnlyText.keyboard)
        return False
    if Mechanic.capture(player=player, sector=sector):
        await msg.answer("Всё заебись, сектор захвачен, отчёт об этом отправлен главе клана", reply_markup=OnlyText.keyboard)
        try:
            await bot.send_message(chat_id=player.fraction.owner.user_id, text=f"Игрок {player.name} захватил сектор [{player.x}{player.y}]\nБой:\nПротивник: {sector_frac.name} {sector_len} Солдат | Атакующий: {player.name} {len(player.warriors)} Солдат\nИтог: ПОБЕДА\nКоординаты сектора: [{player.x};{player.y}]")
            await bot.send_message(chat_id=sector_frac.owner.user_id, text=f"ВАШ СЕКТОР ЗАХВАЧЕН\nНападающий: {player.name} из клана: {player.fraction.name}\nКоординаты сектора: [{player.x};{player.y}]")
        except:
            pass
    else:
        await msg.answer("Твоя атака проебалась, советую оценить потери отряда в статусе")
@router.message(aiogram.filters.StateFilter(Interact.enter))
async def interact_enter(msg: types.Message, state=FSMContext):
    text = msg.text
    if text == "отмена":
        await state.clear()
        await msg.answer("ОК", reply_markup=OnlyText.keyboard)
        return False
    player = players[msg.from_user.id]
    sector = Map.get_sector(player.x, player.y)
    if sector.building.building_type=="work":
        if text.lower()=="работать":
            await msg.answer("Всё ахуенно, ты батрачишь")
            await state.set_state(Buildings.working)
        else:
            await state.clear()
            await msg.answer("Ссыкло ебливое убежал к мамочке плакаться на могилку", reply_markup=OnlyText.keyboard)
    if sector.building.building_type=="warriors":

        frac_war = player.fraction.warriors_types
        i: Classes.Warrior
        for i in frac_war:
            if text==i.name:
                if player.balance>=i.price:
                    player.new_warrior(i)
                    player.balance-=i.price
                    await msg.answer(f"Успешно куплен {i.name}|{i.power}\nПроверь статус отряда", reply_markup=OnlyText.keyboard)
                else:
                    await msg.answer("Нищеебина сьеби с сектора", reply_markup=OnlyText.keyboard)
        await state.clear()

    if sector.building.building_type=="shop":

        i: Classes.Item
        for i in sector.building.items:
            if text==i.name:

                towar = i

                if player.balance>=towar.cost:
                    player.backpack.append(towar)
                    player.balance-=towar.cost
                    sector.building.owner.balance+=(towar.cost*0.1)
                    await msg.answer(f"Товар куплен, текущий баланс: \n{player.balance} шекелей", reply_markup=OnlyText.keyboard)
                else:
                    await msg.answer("хуила нищая сьеби с магазина нахуй", reply_markup=OnlyText.keyboard)
        await state.clear()
    if sector.building.building_type=="casino":
        await state.set_state(Casino.choose)
        kb = [
            [types.KeyboardButton(text="Рулетка(Глобальная)")],

            [types.KeyboardButton(text="Рулетка(В секторе)")],
            [types.KeyboardButton(text="Камень/Ножницы/Бумага")],

            [types.KeyboardButton(text="Очко")],
            [types.KeyboardButton(text="Отмена")]

        ]
        await msg.answer(f"Ебать нахуй, homo ludens решил посетить естественную среду обитания\nВыбирай в каком режиме сосать будешь\n\n{OnlyText.casic_rejim} ", reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))


@router.message(aiogram.filters.StateFilter(Interact.build))
async def interact_building(msg: types.Message, state=FSMContext):
    text = msg.text
    player = players[msg.from_user.id]
    sector = Map.get_sector(player.x, player.y)
    sp = []
    for j in Hip.buildings:
        sp.append(j)
    if text=="Отмена":
        await state.clear()
        await main_page(msg)
    if not(text in sp):
        await msg.answer("АШИБКА КОД IH199\nЖми на кнопки еблан", reply_markup=OnlyText.keyboard)
        await state.clear()
        return False
    building: Hip.Building = Hip.buildings[text]
    if player.balance>=building.price:
        if sector.building.building_type=="void":
            sector.build(Map.Sector.Building(building.name, player, building_type=building.type))
            player.balance-=building.price

            await msg.answer(f"Заебок\nЗдание {building.name} успешно построено\nпереименовать постройку можно в меню взаимодействия", reply_markup=OnlyText.keyboard)
        else:
            await msg.answer("АШИБКА КОД IH210\nНа секторе уже чёта есть", reply_markup=OnlyText.keyboard)

    else:
        await msg.answer("Хуйня нищая, накопи столько сначала", reply_markup=OnlyText.keyboard)
    await state.clear()