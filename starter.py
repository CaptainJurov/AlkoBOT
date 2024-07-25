import aiogram
import asyncio
from Hip import dp, bot
from Modules import Interface


async def main():
    print("starting bot...")
    dp.include_router(Interface.router)
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())
    print("POWER OFF")
