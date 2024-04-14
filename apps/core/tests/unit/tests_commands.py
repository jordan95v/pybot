from unittest.mock import MagicMock
from django.core.management import call_command
from pytest_mock import MockerFixture
from apps.core.pybot import Pybot


class TestCommand:
    def test_launch(self, mocker: MockerFixture) -> None:
        run_mock: MagicMock = mocker.patch.object(Pybot, "run")
        call_command("launch")
        run_mock.assert_called_once()
