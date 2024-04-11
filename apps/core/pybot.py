import discord
from discord.ext import commands
from apps.core.models import Server

__all__: list[str] = ["Pybot"]


class Pybot(commands.Bot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def get_server(self, ctx: commands.Context) -> Server:
        """Get the server from the context.

        Args:
            ctx: The context of the command.

        Returns:
            Server: The server object.
        """

        server: Server
        server, _ = await Server.objects.aget_or_create(discord_id=ctx.guild.id)  # type: ignore
        return server

    async def add_cogs(self, cogs: list[type[commands.Cog]]) -> None:
        """Add a list of cogs to the bot.

        Args:
            cogs: The list of cogs to add.
        """

        for cog in cogs:
            await self.add_cog(cog(self))

    @commands.Cog.listener()
    async def on_command_error(
        self, context: commands.Context, exception: commands.CommandError
    ) -> None:
        if isinstance(exception, commands.MissingRequiredArgument):
            await context.reply("You are missing a required argument. Check help :)")
            return
        await context.reply(
            "An error occurred. Check help or contact an administrator."
        )

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Change the presence of the bot on ready."""

        await self.change_presence(activity=discord.Game(name="!help"))
