from dotenv import dotenv_values
from dataclasses import dataclass


@dataclass
class Cfg:
    TOKEN = dotenv_values()["TOKEN"]
    CHANNEL_ID = dotenv_values()["CHANNEL_ID"]
