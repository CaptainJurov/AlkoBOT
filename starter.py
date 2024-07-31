import aiogram
import asyncio
from Hip import dp, bot
from Modules import Interface, Clan_Handler, Building_Handler, Interact_Handler, Moving_Handler


async def main():
    print("starting bot...")
    dp.include_router(Clan_Handler.router)
    dp.include_router(Interface.router)

    dp.include_router(Building_Handler.router)
    dp.include_router(Interact_Handler.router)
    dp.include_router(Moving_Handler.router)
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())
    print("POWER OFF")
