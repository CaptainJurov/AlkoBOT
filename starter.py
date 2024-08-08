import aiogram
import asyncio
from typing import Callable, Dict, Any, Awaitable
import Hip
from aiogram.types import TelegramObject
import time
import logging
import config
from Hip import dp, bot, players
from aiogram.fsm.context import FSMContext
from Modules import Interface, Clan_Handler, Building_Handler, Interact_Handler, Moving_Handler, Casino, Bank
logging.basicConfig(format='%(asctime)s - [%(levelname)s] - %(message)s', level=logging.DEBUG, filemode="w", filename="bot_log.log")
class SomeMiddleware(aiogram.BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        id = data['event_context'].chat.id
        if int(id) in players:
            player = players[int(id)]
            if not(player.playable):
                if int(time.time()) >= player.time:
                    player.playable = True
                else:
                    result = await bot.send_message(id, text=f"Погоди малясь, осталось {int(player.time-int(time.time()))} секунд")
                    return result
        if int(id) in Hip.banned:
            result = await bot.send_message(id, text="Ты забанен)")
        else:
            result = await handler(event, data)
        return result
async def main():
    print("starting bot...")
    dp.message.middleware(SomeMiddleware())
    dp.callback_query.middleware(SomeMiddleware())
    dp.include_router(Clan_Handler.router)
    dp.include_router(Interface.router)
    dp.include_router(Building_Handler.router)
    dp.include_router(Interact_Handler.router)
    dp.include_router(Bank.router)
    dp.include_router(Casino.router)
    dp.include_router(Moving_Handler.router)

    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())
    print("POWER OFF")
