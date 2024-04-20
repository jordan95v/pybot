import asyncio
from typing import Any
from django.core.management import BaseCommand
import discord
from discord.ext import commands
from apps.core.cogs import AdminCog, StudentCog
from apps.core.pybot import Pybot
from config.app_settings import DISCORD_TOKEN, DISCORD_COMMAND_PREFIX

__all__: list[str] = ["Command"]


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        intents: discord.Intents = discord.Intents.all()
        pybot: Pybot = Pybot(
            command_prefix=DISCORD_COMMAND_PREFIX, intents=intents, help_command=None
        )
        cogs: list[type[commands.Cog]] = [AdminCog, StudentCog]
        asyncio.run(pybot.add_cogs(cogs))
        pybot.run(DISCORD_TOKEN)
