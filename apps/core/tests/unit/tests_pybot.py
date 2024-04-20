from unittest.mock import MagicMock
from discord.ext import commands
import pytest
from pytest_mock import MockerFixture
from apps.core.cogs import AdminCog, StudentCog
from apps.core.models import Server
from apps.core.pybot import Pybot


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
