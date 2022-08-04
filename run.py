from aiogram import executor
from src import handlers
from src.bot import dp, loop, bot, storage
from aiogram.types import BotCommand

handlers.register_handler(dp)


async def on_finish_up(_):
    await storage.close()
    await storage.wait_closed()
    print("Bot Shutdown")


async def setup_bot_commands(_):
    print("Bot Enable")
    cmds = [
        BotCommand(command="/reload", description="Перезагрузить 🔄"),
    ]
    await bot.set_my_commands(cmds)


if __name__ == "__main__":
    executor.start_polling(
        dp,
        loop=loop,
        on_shutdown=on_finish_up,
        skip_updates=True,
        on_startup=setup_bot_commands,
    )
