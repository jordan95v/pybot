import pytest
from discord.ext import commands
from pytest_mock import MockerFixture
from apps.core.pybot import Pybot


@pytest.fixture
def context(mocker: MockerFixture):
    mocker.patch.object(commands.Context, "__init__", return_value=None)
    return commands.Context()  # type: ignore


@pytest.fixture
def pybot(mocker: MockerFixture):
    mocker.patch.object(Pybot, "__init__", return_value=None)
    return Pybot()
