from datetime import datetime
import pytest
from apps.core.models import Student


class TestStudent:
    @pytest.mark.parametrize(
        "last_participation, timestamp, expected",
        [
            (
                None,
                datetime(2021, 1, 2).timestamp(),
                True,
            ),
            (
                datetime(2021, 1, 1),
                datetime(2021, 1, 2).timestamp(),
                True,
            ),
            (
                datetime(2021, 1, 1),
                datetime(2021, 1, 1).timestamp(),
                False,
            ),
            (
                datetime(2021, 1, 2),
                datetime(2021, 1, 1).timestamp(),
                False,
            ),
        ],
    )
    def test_can_participate(
        self, last_participation: float | None, timestamp: float, expected: bool
    ) -> None:
        student: Student = Student(last_participation=last_participation)
        assert student.can_participate(timestamp) == expected
