from datetime import datetime
from unittest.mock import MagicMock
import pytest
from discord.ext import commands
from django.utils import timezone
from pytest_mock import MockerFixture
from apps.core.pybot import Pybot


@pytest.fixture
def context(mocker: MockerFixture):
    mocker.patch.object(commands.Context, "__init__", return_value=None)
    ctx: commands.Context = commands.Context()  # type: ignore
    ctx.message = MagicMock()
    ctx.message.created_at = timezone.make_aware(datetime(2021, 1, 1, 12, 0, 0))
    ctx.guild.id = 9876543210  # type: ignore
    ctx.author.id = 1234567890
    return ctx


@pytest.fixture
def pybot(mocker: MockerFixture):
    mocker.patch.object(Pybot, "__init__", return_value=None)
    return Pybot()
