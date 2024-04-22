from unittest.mock import MagicMock
import discord
import pytest
from discord.ext import commands
from pytest_mock import MockerFixture
from apps.core.cogs import AdminCog, StudentCog
from apps.core.models import Server
from apps.core.pybot import Pybot
from config.app_settings import DISCORD_COMMAND_PREFIX


@pytest.mark.django_db(transaction=True)
class TestPybot:
    async def test_get_server(
        self, pybot: Pybot, context: commands.Context, mocker: MockerFixture
    ) -> None:
        server: Server = await pybot.get_server(context)
        assert isinstance(server, Server)

    @pytest.mark.parametrize(
        "cogs",
        [
            ([AdminCog, StudentCog]),
            ([AdminCog]),
            ([StudentCog]),
        ],
    )
    async def test_add_cogs(
        self, pybot: Pybot, mocker: MockerFixture, cogs: list[type[commands.Cog]]
    ) -> None:
        add_mock: MagicMock = mocker.patch.object(pybot, "add_cog")
        await pybot.add_cogs(cogs)
        assert add_mock.call_count == len(cogs)

    @pytest.mark.parametrize(
        "exception, expected_string",
        [
            (
                commands.MissingRequiredArgument,
                "You are missing a required argument. Check help :)",
            ),
            (
                commands.CommandError,
                "An error occurred. Check help or contact an administrator.",
            ),
        ],
    )
    async def test_on_command_error(
        self,
        pybot: Pybot,
        context: commands.Context,
        mocker: MockerFixture,
        exception: type[commands.CommandError],
        expected_string: str,
    ) -> None:
        reply_mock: MagicMock = mocker.patch.object(context, "reply")
        mocker.patch.object(exception, "__init__", return_value=None)
        await pybot.on_command_error(context, exception())
        reply_mock.assert_called_once_with(expected_string)

    async def test_on_ready(self, pybot: Pybot, mocker: MockerFixture) -> None:
        change_presence_mock: MagicMock = mocker.patch.object(pybot, "change_presence")
        await pybot.on_ready()
        command_name: str = DISCORD_COMMAND_PREFIX + "help"
        change_presence_mock.assert_called_once_with(
            activity=discord.Game(name=command_name)
        )
