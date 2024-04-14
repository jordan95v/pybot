from unittest.mock import MagicMock
import pytest
from discord.ext import commands
from pytest_mock import MockerFixture
from apps.core.pybot import Pybot


@pytest.fixture
def context(mocker: MockerFixture):
    mocker.patch.object(commands.Context, "__init__", return_value=None)
    mocker.patch.object(commands.Context, "author")
    mocker.patch.object(commands.Context.author, "id", 1234567890)
    return commands.Context()  # type: ignore


@pytest.fixture
def pybot(mocker: MockerFixture):
    mocker.patch.object(Pybot, "__init__", return_value=None)
    return Pybot()
