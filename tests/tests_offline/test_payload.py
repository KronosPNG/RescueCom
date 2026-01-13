import pytest
import uuid
from offline.payload import Payload


def test_payload_valid():
    p = Payload(
        user_uuid=str(uuid.uuid4()),
        emergency_id=10,
        severity=200,
        position=(45.0, 9.0),
    )
    data = p.pack_data()
    assert isinstance(data, bytes)
    assert len(data) == 20


def test_invalid_uuid():
    with pytest.raises(ValueError):
        Payload(
            user_uuid="not-a-uuid",
            emergency_id=1,
            severity=1,
            position=(0.0, 0.0),
        )


def test_emergency_id_negative():
    with pytest.raises(ValueError):
        Payload(
            user_uuid=str(uuid.uuid4()),
            emergency_id=-1,
            severity=1,
            position=(0.0, 0.0),
        )


def test_emergency_id_out_of_range():
    with pytest.raises(ValueError):
        Payload(
            user_uuid=str(uuid.uuid4()),
            emergency_id=64,
            severity=1,
            position=(0.0, 0.0),
        )


def test_severity_out_of_range():
    with pytest.raises(ValueError):
        Payload(
            user_uuid=str(uuid.uuid4()),
            emergency_id=1,
            severity=256,
            position=(0.0, 0.0),
        )


def test_position_not_tuple():
    with pytest.raises(ValueError):
        Payload(
            user_uuid=str(uuid.uuid4()),
            emergency_id=1,
            severity=1,
            position=[0.0, 0.0],
        )


def test_position_wrong_length():
    with pytest.raises(ValueError):
        Payload(
            user_uuid=str(uuid.uuid4()),
            emergency_id=1,
            severity=1,
            position=(0.0,),
        )


def test_latitude_out_of_range():
    with pytest.raises(ValueError):
        Payload(
            user_uuid=str(uuid.uuid4()),
            emergency_id=1,
            severity=1,
            position=(100.0, 0.0),
        )


def test_longitude_out_of_range():
    with pytest.raises(ValueError):
        Payload(
            user_uuid=str(uuid.uuid4()),
            emergency_id=1,
            severity=1,
            position=(0.0, 200.0),
        )


def test_unpack_data_too_short():
    with pytest.raises(Exception):
        Payload.unpack_data(b"\x00" * 10)


def test_pack_unpack_roundtrip():
    p1 = Payload(
        user_uuid=str(uuid.uuid4()),
        emergency_id=12,
        severity=34,
        position=(12.5, -45.8),
    )
    data = p1.pack_data()
    p2 = Payload.unpack_data(data)

    assert p1.user_uuid == p2.user_uuid
    assert p1.emergency_id == p2.emergency_id
    assert p1.severity == p2.severity
    assert abs(p1.position[0] - p2.position[0]) < 1
    assert abs(p1.position[1] - p2.position[1]) < 1
