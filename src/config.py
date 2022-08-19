import os
from dataclasses import dataclass


@dataclass
class Cfg:
    TOKEN = os.environ.get("TOKEN")
    CHANNEL_ID = os.environ.get("CHANNEL_ID")