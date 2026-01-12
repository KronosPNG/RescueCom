import pytest
import datetime

from common.models.enc_emergency import EncryptedEmergency


@pytest.fixture
def encrypted_emergency_factory():
    def _factory():
        return EncryptedEmergency(
            emergency_id=1,
            user_uuid="user-uuid",
            severity=30,
            routing_info_json='{"a": 1}',
            blob=b"encrypted_payload",
            created_at=datetime.datetime(
                2024, 1, 1, 12, 0, 0
            ),  # Manual datetime for testing purposes
        )

    return _factory


def test_to_db_tuple_content(encrypted_emergency_factory):
    eem = encrypted_emergency_factory()
    db_tuple = eem.to_db_tuple()

    assert isinstance(db_tuple, tuple)
    assert len(db_tuple) == 6

    assert db_tuple[0] == 1  # emergency_id
    assert db_tuple[1] == "user-uuid"  # user_uuid
    assert db_tuple[2] == 30  # severity
    assert db_tuple[3] == '{"a": 1}'  # routing_info_json
    assert db_tuple[4] == b"encrypted_payload"  # blob
    assert db_tuple[5] == datetime.datetime(2024, 1, 1, 12, 0, 0)  # created_at
