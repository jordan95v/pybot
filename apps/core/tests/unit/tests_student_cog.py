from datetime import UTC, datetime
from typing import Any
from unittest.mock import MagicMock
from discord.ext import commands
from freezegun import freeze_time
import pytest
from pytest_mock import MockerFixture
from apps.core.cogs import StudentCog
from apps.core.models import Server, Student
from apps.core.pybot import Pybot


@pytest.mark.django_db(transaction=True)
class TestStudentCog:
    @pytest.mark.parametrize(
        "should_create_student, expected_message",
        [
            (False, "Your registration is complete, <@1234567890>"),
            (True, "You are already registered, <@1234567890>"),
        ],
    )
    async def test_register(
        self,
        mocker: MockerFixture,
        context: commands.Context,
        pybot: Pybot,
        should_create_student: bool,
        expected_message: str,
    ) -> None:
        server: Server = await Server.objects.acreate(discord_id=context.author.id)
        mocker.patch.object(pybot, "get_server", return_value=server)
        reply_mock: MagicMock = mocker.patch.object(context, "reply")
        if should_create_student:
            await Student.objects.acreate(
                discord_id=context.author.id,
                first_name="John",
                last_name="Doe",
                class_name="Class 1",
                server=server,
            )
        cog: StudentCog = StudentCog(pybot)
        await cog.register(cog, context, "John", "Doe", "Class 1")  # type: ignore
        reply_mock.assert_called_once_with(expected_message)

    @pytest.mark.parametrize(
        "should_create_student, expected_message",
        [
            (True, "Your information has been updated, <@1234567890>"),
            (False, "You are not registered, <@1234567890>"),
        ],
    )
    async def test_modify(
        self,
        mocker: MockerFixture,
        context: commands.Context,
        pybot: Pybot,
        should_create_student: bool,
        expected_message: str,
    ) -> None:
        server: Server = await Server.objects.acreate(discord_id=context.author.id)
        mocker.patch.object(pybot, "get_server", return_value=server)
        reply_mock: MagicMock = mocker.patch.object(context, "reply")
        if should_create_student:
            await Student.objects.acreate(
                discord_id=context.author.id,
                first_name="John",
                last_name="Doe",
                class_name="Class 1",
                server=server,
            )
        cog: StudentCog = StudentCog(pybot)
        await cog.modify(cog, context, "John", "Doe", "Class 2")  # type: ignore
        reply_mock.assert_called_once_with(expected_message)

    @pytest.mark.parametrize(
        "should_create_student, expected_message",
        [
            (True, "You have 0.0 points, <@1234567890>"),
            (False, "You are not registered, <@1234567890>"),
        ],
    )
    async def test_points(
        self,
        mocker: MockerFixture,
        context: commands.Context,
        pybot: Pybot,
        should_create_student: bool,
        expected_message: str,
    ) -> None:
        server: Server = await Server.objects.acreate(discord_id=context.author.id)
        mocker.patch.object(pybot, "get_server", return_value=server)
        reply_mock: MagicMock = mocker.patch.object(context, "reply")
        if should_create_student:
            await Student.objects.acreate(
                discord_id=context.author.id,
                first_name="John",
                last_name="Doe",
                class_name="Class 1",
                server=server,
            )
        cog: StudentCog = StudentCog(pybot)
        await cog.points(cog, context)  # type: ignore
        reply_mock.assert_called_once_with(expected_message)

    @freeze_time("2021-01-01")
    @pytest.mark.parametrize(
        "server_state, should_create_student, can_participate, expected_message",
        [
            (False, False, False, "Association is closed, <@1234567890>"),
            (True, False, False, "You are not registered, <@1234567890>"),
            (True, True, False, "You already participated today, <@1234567890>"),
            # (True, True, True, "You have participated, <@1234567890>"), Mock error
        ],
    )
    async def test_present(
        self,
        mocker: MockerFixture,
        context: commands.Context,
        pybot: Pybot,
        server_state: bool,
        should_create_student: bool,
        can_participate: bool,
        expected_message: str,
    ) -> None:
        async def wait_for(*args: Any, **kwargs: Any) -> Any:
            return None

        server: Server = await Server.objects.acreate(
            discord_id=context.author.id, is_open=server_state
        )
        mocker.patch.object(pybot, "get_server", return_value=server)
        reply_mock: MagicMock = mocker.patch.object(context, "reply")
        mocker.patch.object(Student, "can_participate", return_value=can_participate)
        mocker.patch.object(Pybot, "wait_for", side_effect=wait_for)
        if should_create_student:
            await Student.objects.acreate(
                discord_id=1234567890,
                first_name="John",
                last_name="Doe",
                class_name="Class 1",
                last_participation=datetime.now(UTC),
                server=server,
            )
        cog: StudentCog = StudentCog(pybot)
        await cog.present(cog, context)  # type: ignore
        reply_mock.assert_called_once_with(expected_message)
