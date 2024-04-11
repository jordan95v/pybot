from discord.ext import commands
from apps.core.models import Server
from apps.core.pybot import Pybot


class AdminCog(commands.Cog):
    def __init__(self, bot: Pybot):
        self.bot = bot

    @commands.command(name="change_points")
    @commands.has_permissions(administrator=True)
    async def change_points(self, ctx: commands.Context, points: float) -> None:
        server: Server = await self.bot.get_server(ctx)
        server.points_to_give = points
        await server.asave()

    @commands.command(name="switch")
    @commands.has_permissions(administrator=True)
    async def switch(self, ctx: commands.Context) -> None:
        server: Server = await self.bot.get_server(ctx)
        server.is_open = not server.is_open
        await server.asave()

    @commands.command(name="status")
    @commands.has_permissions(administrator=True)
    async def status(self, ctx: commands.Context) -> None:
        server: Server = await self.bot.get_server(ctx)
        await ctx.reply(f"Association is {'open' if server.is_open else 'closed'}")
