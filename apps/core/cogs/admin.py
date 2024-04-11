from discord.ext import commands
from apps.core.models import Server, Student
from apps.core.pybot import Pybot

__all__: list[str] = ["AdminCog"]


class AdminCog(commands.Cog):
    def __init__(self, bot: Pybot):
        self.bot = bot

    @commands.command(name="change_points")
    @commands.has_permissions(administrator=True)
    async def change_points(self, ctx: commands.Context, points: float) -> None:
        """Change the points to give for each participation.

        Args:
            ctx: The context of the command.
            points: The new points to give to each student per participation.
        """

        server: Server = await self.bot.get_server(ctx)
        server.points_to_give = points
        await server.asave()

    @commands.command(name="switch")
    @commands.has_permissions(administrator=True)
    async def switch(self, ctx: commands.Context) -> None:
        """Switch the association status between open and closed.

        Args:
            ctx: The context of the command.
        """

        server: Server = await self.bot.get_server(ctx)
        server.is_open = not server.is_open
        await server.asave()
        await ctx.reply(f"Association is now {'open' if server.is_open else 'closed'}")

    @commands.command(name="status")
    @commands.has_permissions(administrator=True)
    async def status(self, ctx: commands.Context) -> None:
        """Get the current status of the association.

        Args:
            ctx: The context of the command.
        """

        server: Server = await self.bot.get_server(ctx)
        await ctx.reply(f"Association is {'open' if server.is_open else 'closed'}")

    @commands.command(name="set_points")
    @commands.has_permissions(administrator=True)
    async def set_points(
        self, ctx: commands.Context, points: float, discord_id: int
    ) -> None:
        """Set the points of a student.

        Args:
            ctx: The context of the command.
            points: The new points of the student.
            discord_id: The Discord ID of the student.
        """

        server: Server = await self.bot.get_server(ctx)
        try:
            student: Student = await Student.objects.aget(
                discord_id=discord_id, server=server
            )
        except Student.DoesNotExist:
            await ctx.reply(f"{discord_id} is not registered")
            return
        student.points = points
        await student.asave()
        await ctx.reply(
            f"{student.first_name} {student.last_name} now has {points} points"
        )
