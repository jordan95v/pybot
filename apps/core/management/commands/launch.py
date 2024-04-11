from typing import Any
from django.core.management import BaseCommand
import discord
from config.app_settings import DISCORD_TOKEN
from apps.core.pybot import Pybot

__all__ = ["Command"]


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        intents: discord.Intents = discord.Intents.all()
        pybot: Pybot = Pybot(command_prefix="!", intents=intents)
        pybot.run(DISCORD_TOKEN)
