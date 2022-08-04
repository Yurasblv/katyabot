from aiogram import executor
from src import handlers
from src.bot import dp, loop, bot
from aiogram.types import BotCommand

handlers.register_handler(dp)


async def on_finish_up(_):
    print("Bot Done")


async def setup_bot_commands(_):
    print("Bot Enable")
    cmds = [
        BotCommand(command="/reload", description="Enable Bot"),
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
