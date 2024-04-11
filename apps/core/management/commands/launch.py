import asyncio
from typing import Any
from django.core.management import BaseCommand
import discord
from discord.ext import commands
from apps.core.cogs import AdminCog, StudentCog
from apps.core.pybot import Pybot
from config.app_settings import DISCORD_TOKEN

__all__ = ["Command"]


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        intents: discord.Intents = discord.Intents.all()
        pybot: Pybot = Pybot(command_prefix="?", intents=intents)
        cogs: list[type[commands.Cog]] = [AdminCog, StudentCog]
        asyncio.run(pybot.add_cogs(cogs))
        pybot.run(DISCORD_TOKEN)
