import pytest
import datetime

from common.models.emergency import Emergency
from tests.utils import not_raises


# ---- Fixtures ----


@pytest.fixture
def emergency_factory():
    # Factory to create a dummy Emergency
    def _factory():
        return Emergency(
            emergency_id=1,
            user_uuid="user-uuid",
            severity=30,
            emergency_type="Test type",
            description="Test description",
            created_at=datetime.datetime(
                2024, 1, 1, 12, 0, 0
            ),  # Manual datetime for testing purposes
            address="Via Roma",
            city="Roma",
            street_number=10,
            resolved=False,
            position=(12.34, 56.78),
            place_description="Near park",
            photo_b64="aaaa",
            details_json='{"a": 1}',
        )

    return _factory


@pytest.fixture
def base_kwargs():
    return dict(
        emergency_id=42,
        user_uuid="uuid-123",
        emergency_type="type",
        description="desc",
        created_at=datetime.datetime(2024, 1, 1, 0, 0, 0),
        street_number=10,
    )


# ---- Tests ----


def test_to_db_tuple(emergency_factory):
    em = emergency_factory()
    db_tuple = em.to_db_tuple()

    assert isinstance(db_tuple, tuple)
    assert len(db_tuple) == 14

    assert db_tuple[0] == 1  # emergency_id
    assert db_tuple[1] == "user-uuid"  # user_uuid
    assert db_tuple[2] == "12.34,56.78"  # position
    assert db_tuple[3] == "Via Roma"  # address
    assert db_tuple[4] == "Roma"  # city
    assert db_tuple[5] == 10  # street_number
    assert db_tuple[6] == "Near park"  # place_description
    assert db_tuple[7] == "aaaa"  # photo_b64
    assert db_tuple[8] == 30  # severity
    assert db_tuple[9] is False  # resolved
    assert db_tuple[10] == "Test type"  # emergency_type
    assert db_tuple[11] == "Test description"  # description
    assert db_tuple[12] == '{"a": 1}'  # details_json
    assert db_tuple[13] == datetime.datetime(2024, 1, 1, 12, 0, 0)  # created_at


def test_pack_returns_bytes(emergency_factory):
    em = emergency_factory()
    packed = em.pack()

    assert isinstance(packed, bytes)
    assert len(packed) > 0


def test_pack_unpack_roundtrip(emergency_factory):
    em = emergency_factory()
    packed = em.pack()

    unpacked = Emergency.unpack(
        emergency_id=em.emergency_id,
        user_uuid=em.user_uuid,
        data=packed,
    )

    assert isinstance(unpacked, Emergency)

    assert unpacked.emergency_id == em.emergency_id
    assert unpacked.user_uuid == em.user_uuid
    assert unpacked.address == em.address
    assert unpacked.city == em.city
    assert unpacked.street_number == em.street_number
    assert unpacked.place_description == em.place_description
    assert unpacked.photo_b64 == em.photo_b64
    assert unpacked.severity == em.severity
    assert unpacked.resolved == em.resolved
    assert unpacked.emergency_type == em.emergency_type
    assert unpacked.description == em.description
    assert unpacked.details_json == em.details_json
    assert unpacked.created_at == em.created_at


def test_unpack_wrong_types(emergency_factory):
    em = emergency_factory()
    with pytest.raises(TypeError):
        em.unpack(
            emergency_id="1",
            user_uuid="uuid",
            data=b"bytes",
        )

    with pytest.raises(TypeError):
        em.unpack(
            emergency_id=1,
            user_uuid=123,
            data=b"bytes",
        )

    with pytest.raises(TypeError):
        em.unpack(
            emergency_id=1,
            user_uuid="uuid",
            data="not-bytes",
        )


def test_unpack_corrupted_data(emergency_factory):
    em = emergency_factory()

    with pytest.raises(ValueError):
        em.unpack(
            emergency_id=1,
            user_uuid="uuid",
            data=b"\x00\x00\x00\x05abc",  # Incomplete blob
        )


def test_unpack_not_raises_index_error(emergency_factory):
    em = emergency_factory()
    packed = em.pack()

    with not_raises(IndexError):
        Emergency.unpack(
            emergency_id=em.emergency_id,
            user_uuid=em.user_uuid,
            data=packed,
        )


def test_created_at_invalid_format_raises(emergency_factory):
    # valid blob except `created_at`
    em = emergency_factory()
    packed = em.pack()
    corrupted = packed[:-10] + b"\x00\x00\x00\x03abc"

    with pytest.raises(ValueError):
        Emergency.unpack(
            emergency_id=1,
            user_uuid=em.user_uuid,
            data=corrupted,
        )


# ---- Tests with Category Partition ----


@pytest.mark.parametrize(
    "position",
    [
        (0.0, 0.0),  # zero
        (12.5, 99.9),  # tipical values
        (-12.5, -99.9),  # negatives
        (1e10, -1e10),  # extrems
    ],
)
def test_position_partitions(base_kwargs, position):
    e = Emergency(**base_kwargs, severity=1, position=position)
    packed = e.pack()

    unpacked = Emergency.unpack(
        emergency_id=e.emergency_id,
        user_uuid=e.user_uuid,
        data=packed,
    )

    assert unpacked.position == tuple(map(str, position))


@pytest.mark.parametrize("severity", [0, 1, 5, 2**31 - 1])
def test_severity_partitions(base_kwargs, severity):
    e = Emergency(severity=severity, **base_kwargs)
    packed = e.pack()

    unpacked = Emergency.unpack(
        emergency_id=e.emergency_id,
        user_uuid=e.user_uuid,
        data=packed,
    )

    assert unpacked.severity == severity


@pytest.mark.parametrize("resolved", [True, False])
def test_resolved_partitions(base_kwargs, resolved):
    e = Emergency(resolved=resolved, severity=1, **base_kwargs)
    packed = e.pack()

    unpacked = Emergency.unpack(
        emergency_id=e.emergency_id,
        user_uuid=e.user_uuid,
        data=packed,
    )

    assert unpacked.resolved is resolved


@pytest.mark.parametrize(
    "value",
    [
        "abc",  # normal
        "",  # empty
        "x" * 10_000,  # long
    ],
)
def test_string_field_partitions(value):
    e = Emergency(
        emergency_id=1,
        user_uuid="user-uuid",
        severity=30,
        emergency_type=value,
        description=value,
        created_at=datetime.datetime(
            2024, 1, 1, 12, 0, 0
        ),  # Manual datetime for testing purposes
        address=value,
        city=value,
        street_number=10,
        resolved=False,
        position=(12.34, 56.78),
        place_description=value,
        photo_b64=value,
        details_json=value,
    )

    packed = e.pack()
    unpacked = Emergency.unpack(
        emergency_id=e.emergency_id,
        user_uuid=e.user_uuid,
        data=packed,
    )

    assert unpacked.address == value
    assert unpacked.city == value
    assert unpacked.place_description == value
    assert unpacked.photo_b64 == value
    assert unpacked.emergency_type == value
    assert unpacked.description == value
    assert unpacked.details_json == value


@pytest.mark.parametrize(
    "created_at",
    [
        datetime.datetime(1970, 1, 1),
        datetime.datetime.now(),
        datetime.datetime(9999, 12, 31, 23, 59, 59),
    ],
)
def test_created_at_partitions(created_at):
    e = Emergency(
        emergency_id=1,
        user_uuid="user-uuid",
        severity=30,
        emergency_type="Test type",
        description="Test description",
        created_at=created_at,
        address="Via Roma",
        city="Roma",
        street_number=10,
        resolved=False,
        position=(12.34, 56.78),
        place_description="Near park",
        photo_b64="aaaa",
        details_json='{"a": 1}',
    )
    packed = e.pack()

    unpacked = Emergency.unpack(
        emergency_id=e.emergency_id,
        user_uuid=e.user_uuid,
        data=packed,
    )

    assert unpacked.created_at == created_at
