import csv
from unittest.mock import MagicMock
import pytest
from discord.ext import commands
from pytest_mock import MockerFixture
from apps.core.cogs import AdminCog
from apps.core.models import Server, Student
from apps.core.pybot import Pybot


@pytest.mark.django_db(transaction=True)
class TestAdminCog:
    @pytest.mark.parametrize("points", [10, 20, 30])
    async def test_change_points(
        self,
        pybot: Pybot,
        context: commands.Context,
        mocker: MockerFixture,
        points: float,
    ) -> None:
        server: Server = await Server.objects.acreate(discord_id=context.guild.id)  # type: ignore
        mocker.patch.object(Pybot, "get_server", return_value=server)
        cog: AdminCog = AdminCog(pybot)
        await cog.change_points(cog, context, points)  # type: ignore
        await server.arefresh_from_db()
        assert server.points_to_give == points

    @pytest.mark.parametrize(
        "base_state, expected_state",
        [(True, False), (False, True)],
    )
    async def test_switch(
        self,
        pybot: Pybot,
        context: commands.Context,
        mocker: MockerFixture,
        base_state: bool,
        expected_state: bool,
    ) -> None:
        server: Server = await Server.objects.acreate(
            discord_id=context.guild.id, is_open=base_state  # type: ignore
        )
        mocker.patch.object(Pybot, "get_server", return_value=server)
        reply_mock: MagicMock = mocker.patch.object(
            commands.Context, "reply", return_value=None
        )
        cog: AdminCog = AdminCog(pybot)
        await cog.switch(cog, context)  # type: ignore
        await server.arefresh_from_db()
        assert server.is_open == expected_state
        reply_mock.assert_called_once_with(
            f"Association is now {'open' if server.is_open else 'closed'}"
        )

    @pytest.mark.parametrize(
        "points, discord_id, should_create_student",
        [
            (10, 123456789, True),
            (20, 987654321, False),
        ],
    )
    async def test_set_points(
        self,
        pybot: Pybot,
        context: commands.Context,
        mocker: MockerFixture,
        points: float,
        discord_id: int,
        should_create_student: bool,
    ) -> None:
        server: Server = await Server.objects.acreate(discord_id=context.guild.id)  # type: ignore
        mocker.patch.object(Pybot, "get_server", return_value=server)
        reply_mock: MagicMock = mocker.patch.object(
            commands.Context, "reply", return_value=None
        )
        cog: AdminCog = AdminCog(pybot)
        if not should_create_student:
            await cog.set_points(cog, context, points, discord_id)  # type: ignore
            reply_mock.assert_called_once_with(f"{discord_id} is not registered")
            return
        student: Student = await Student.objects.acreate(
            discord_id=discord_id, first_name="John", last_name="Doe", server=server
        )
        await cog.set_points(cog, context, points, discord_id)  # type: ignore
        await student.arefresh_from_db()
        assert student.points == points

    @pytest.mark.parametrize(
        "student_count",
        [0, 1, 2],
    )
    async def test_export(
        self,
        pybot: Pybot,
        context: commands.Context,
        mocker: MockerFixture,
        student_count: int,
    ) -> None:
        server: Server = await Server.objects.acreate(discord_id=context.guild.id)  # type: ignore
        for i in range(student_count):
            await Student.objects.acreate(
                discord_id=123456789 + i,
                first_name=f"John{i}",
                last_name=f"Doe{i}",
                server=server,
            )
        write_row_mock: MagicMock = mocker.patch.object(
            csv.DictWriter, "writerow", return_value=None
        )
        reply_mock: MagicMock = mocker.patch.object(
            commands.Context, "reply", return_value=None
        )
        cog: AdminCog = AdminCog(pybot)
        await cog.export(cog, context)  # type: ignore
        reply_mock.assert_called_once()
        assert write_row_mock.call_count == student_count
