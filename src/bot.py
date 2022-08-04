from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from src.config import Cfg
import asyncio
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
loop = asyncio.get_event_loop()
bot = Bot(token=Cfg.TOKEN, loop=loop)
storage = RedisStorage2("redis", 6379, db=5)
dp = Dispatcher(bot, storage=storage)
