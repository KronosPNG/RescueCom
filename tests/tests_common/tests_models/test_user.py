import datetime
import pytest

from common.models.user import User, BloodType


@pytest.fixture
def user_factory():
    def _factory():
        return User(
            uuid="user-uuid",
            is_rescuer=True,
            name="Mario",
            surname="Rossi",
            birthday=datetime.date(1990, 1, 1),
            blood_type=BloodType.ONEG,
            health_info_json='{"test": []}',
        )

    return _factory


def test_to_db_tuple(user_factory):
    u = user_factory()
    result = u.to_db_tuple()

    assert isinstance(result, tuple)
    assert len(result) == 7

    assert result[0] == "user-uuid"  # uuid
    assert result[1]  # is_rescuer (should be True)
    assert result[2] == "Mario"  # name
    assert result[3] == "Rossi"  # surname
    assert result[4] == datetime.date(1990, 1, 1)  # birthday
    assert (
        result[5] == BloodType.ONEG.name
    )  # blood_type (The enum name (BloodType.ONEG -> "ONEG"))
    assert result[6] == '{"test": []}'  # health_info_json
