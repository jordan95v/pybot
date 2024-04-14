import discord
from discord.ext import commands
from apps.core.models import Server, Student
from apps.core.pybot import Pybot

__all__: list[str] = ["StudentCog"]


class StudentCog(commands.Cog):
    def __init__(self, bot: Pybot) -> None:
        self.bot = bot

    @commands.command(name="register")
    async def register(
        self, ctx: commands.Context, first_name: str, last_name: str, class_name: str
    ) -> None:
        """Register a student.

        Args:
            ctx: The context of the command.
            first_name: The first name of the student.
            last_name: The last name of the student.
            class_name: The class name of the student.
        """

        server: Server = await self.bot.get_server(ctx)
        try:
            await Student.objects.aget(discord_id=ctx.author.id, server=server)
            await ctx.reply(f"You are already registered, <@{ctx.author.id}>")
        except Student.DoesNotExist:
            await Student.objects.acreate(
                discord_id=ctx.author.id,
                first_name=first_name,
                last_name=last_name,
                class_name=class_name,
                server=server,
            )
            await ctx.reply(f"Your registration is complete, <@{ctx.author.id}>")

    @commands.command(name="modify")
    async def modify(
        self, ctx: commands.Context, first_name: str, last_name: str, class_name: str
    ) -> None:
        """Modify the information of a student.

        Args:
            ctx: The context of the command.
            first_name: The new first name of the student.
            last_name: The new last name of the student.
            class_name: The new class name of the student.
        """

        server: Server = await self.bot.get_server(ctx)
        try:
            student: Student = await Student.objects.aget(
                discord_id=ctx.author.id, server=server
            )
        except Student.DoesNotExist:
            await ctx.reply(f"You are not registered, <@{ctx.author.id}>")
            return
        student.first_name = first_name
        student.last_name = last_name
        student.class_name = class_name
        await student.asave()
        await ctx.reply(f"Your information has been updated, <@{ctx.author.id}>")

    @commands.command(name="points")
    async def points(self, ctx: commands.Context) -> None:
        """Get the points of a student.

        Args:
            ctx: The context of the command.
        """

        server: Server = await self.bot.get_server(ctx)
        try:
            student: Student = await Student.objects.aget(
                discord_id=ctx.author.id, server=server
            )
        except Student.DoesNotExist:
            await ctx.reply(f"You are not registered, <@{ctx.author.id}>")
            return
        await ctx.reply(f"You have {student.points} points, <@{ctx.author.id}>")

    @commands.command(name="present")
    async def present(self, ctx: commands.Context) -> None:
        """Participate in the association.

        Args:
            ctx: The context of the command.
        """

        def check(reaction: discord.Reaction, user: discord.Member) -> bool:
            return (
                reaction.message.id == ctx.message.id
                and user.guild_permissions.administrator
            )

        server: Server = await self.bot.get_server(ctx)
        if not server.is_open:
            await ctx.reply(f"Association is closed, <@{ctx.author.id}>")
            return
        try:
            student: Student = await Student.objects.aget(
                discord_id=ctx.author.id, server=server
            )
        except Student.DoesNotExist:
            await ctx.reply(f"You are not registered, <@{ctx.author.id}>")
            return
        if not student.can_participate(ctx.message.created_at.timestamp()):
            await ctx.reply(f"You already participated today, <@{ctx.author.id}>")
            return
        await self.bot.wait_for("reaction_add", check=check)
        student.points += server.points_to_give
        student.last_participation = ctx.message.created_at
        await student.asave()
        await ctx.reply(f"You have participated, <@{ctx.author.id}>")
