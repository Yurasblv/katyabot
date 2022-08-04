from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
import logging
from src.config import Cfg

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
loop = asyncio.get_event_loop()
bot = Bot(token=Cfg.TOKEN, loop=loop)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
