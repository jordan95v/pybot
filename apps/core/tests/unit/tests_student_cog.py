from unittest.mock import MagicMock
from discord.ext import commands
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
