import discord
from discord.ext import commands


class Pybot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Change the presence of the bot on ready."""

        await self.change_presence(activity=discord.Game(name="!help"))
