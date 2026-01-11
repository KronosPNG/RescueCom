from datetime import datetime, timedelta

import pytest

from common.models.emergency import Emergency
from common.models.enc_emergency import EncryptedEmergency
from common.services.emergency_queue import EmergencyQueue, SeverityType
from tests.utils import not_raises

# ---- Fixtures ----


@pytest.fixture
def emergency_queue():
    # Reset singleton for each test
    EmergencyQueue.__instance = None
    eq = EmergencyQueue.get_instance()
    eq.low_queue.clear()
    eq.medium_queue.clear()
    eq.high_queue.clear()
    return eq


@pytest.fixture
def emergency_factory():
    # Factory to create a dummy Emergency
    def _factory(severity=10, user_uuid="user1", emergency_id=1, created_at=None):
        created_at = created_at or datetime.now()
        em = Emergency(
            severity=severity,
            user_uuid=user_uuid,
            emergency_id=emergency_id,
            created_at=created_at,
            emergency_type="emergency_test",
            description="Test description",
        )
        return em

    return _factory


@pytest.fixture
def encrypted_emergency_factory():
    # Factory to create a dummy EncryptedEmergency
    def _factory(severity=10, user_uuid="user_enc", emergency_id=1, created_at=None):
        created_at = created_at or datetime.now()
        em = EncryptedEmergency(
            severity=severity,
            user_uuid=user_uuid,
            emergency_id=emergency_id,
            created_at=created_at,
            routing_info_json="{}",
            blob=b"encrypted_blob",
        )
        return em

    return _factory


# ---- Tests ----


def test_singleton(emergency_queue):
    q1 = emergency_queue
    q2 = EmergencyQueue.get_instance()
    assert q1 is q2  # Must be the same object


def test_push_and_pop_low(emergency_queue, emergency_factory):
    em1 = emergency_factory(severity=10)
    em2 = emergency_factory(severity=20, user_uuid="user2", emergency_id=2)
    emergency_queue.push_emergency(em1)
    emergency_queue.push_emergency(em2)

    popped = emergency_queue.pop_emergency(SeverityType.LOW)
    assert popped in [em1, em2]


def test_push_and_pop_medium_high(emergency_queue, emergency_factory):
    em_medium = emergency_factory(severity=40)
    em_high = emergency_factory(severity=70)

    emergency_queue.push_emergency(em_medium)
    emergency_queue.push_emergency(em_high)

    assert emergency_queue.pop_emergency(SeverityType.MEDIUM) is em_medium
    assert emergency_queue.pop_emergency(SeverityType.HIGH) is em_high


def test_pop_empty_raises(emergency_queue):
    with pytest.raises(IndexError):
        emergency_queue.pop_emergency(SeverityType.LOW)


def test_update_emergency(emergency_queue, emergency_factory):
    em = emergency_factory(severity=10)
    emergency_queue.push_emergency(em)

    # Modify and update
    updated_em = emergency_factory(
        severity=50, user_uuid=em.user_uuid, emergency_id=em.emergency_id
    )
    emergency_queue.update_emergency(
        old_emergency_severity=em.severity, emergency=updated_em
    )

    popped = emergency_queue.pop_emergency(SeverityType.MEDIUM)
    assert popped is updated_em


def test_update_nonexistent_raises(emergency_queue, emergency_factory):
    em = emergency_factory(severity=10)

    # Not inserted, so update should fail
    with pytest.raises(ValueError):
        emergency_queue.update_emergency(
            old_emergency_severity=em.severity, emergency=em
        )


def test_mixed_emergencies(
    emergency_queue, emergency_factory, encrypted_emergency_factory
):
    em1 = emergency_factory(severity=5)
    em2 = encrypted_emergency_factory(severity=60)
    emergency_queue.push_emergency(em1)
    emergency_queue.push_emergency(em2)

    # Control pop in both levels
    assert emergency_queue.pop_emergency(SeverityType.LOW) is em1
    assert emergency_queue.pop_emergency(SeverityType.MEDIUM) is em2


def test_multiple_same_severity_ordering(emergency_queue, emergency_factory):
    now = datetime.now()
    em1 = emergency_factory(severity=10, created_at=now)
    em2 = emergency_factory(severity=10, created_at=now + timedelta(seconds=10))
    emergency_queue.push_emergency(em1)
    emergency_queue.push_emergency(em2)

    # em1 has a more recent timestamp, so it has priority
    assert emergency_queue.pop_emergency(SeverityType.LOW) is em1


def test_push_emergency_not_raises(
    emergency_queue, emergency_factory, encrypted_emergency_factory
):
    valid_inputs = [
        emergency_factory(severity=5),
        emergency_factory(severity=40),
        emergency_factory(severity=70),
        encrypted_emergency_factory(severity=15),
        encrypted_emergency_factory(severity=50),
        encrypted_emergency_factory(severity=80),
    ]

    for em in valid_inputs:
        with not_raises(Exception):
            emergency_queue.push_emergency(em)


def test_update_emergency_not_raises(emergency_queue, emergency_factory):
    em = emergency_factory(severity=10)
    emergency_queue.push_emergency(em)

    updated_em = emergency_factory(
        severity=50, user_uuid=em.user_uuid, emergency_id=em.emergency_id
    )

    with not_raises(Exception):
        emergency_queue.update_emergency(
            old_emergency_severity=em.severity, emergency=updated_em
        )


# ---- Tests with Category Partition ----


@pytest.mark.parametrize(
    "severity,factory_name,expect_no_raise",
    [
        # Valid cases: low, medium, high with Emergency
        (10, "emergency_factory", True),
        (40, "emergency_factory", True),
        (70, "emergency_factory", True),
        # Valid cases: low, medium, high with EncryptedEmergency
        (10, "encrypted_emergency_factory", True),
        (40, "encrypted_emergency_factory", True),
        (70, "encrypted_emergency_factory", True),
        # TODO: change as soon PR https://github.com/KronosPNG/RescueCom/pull/47 will be merged
        # Invalid severity (not yet defined) in the logic
        # because the logic puts >=65 in high
        (-1, "emergency_factory", True),
        (999, "emergency_factory", True),
    ],
)
def test_push_emergencies_category_partition(
    emergency_queue, request, severity, factory_name, expect_no_raise
):
    em_factory = request.getfixturevalue(factory_name)
    em = em_factory(severity=severity)

    if expect_no_raise:
        emergency_queue.push_emergency(em)
    else:
        with pytest.raises(Exception):
            emergency_queue.push_emergency(em)


@pytest.mark.parametrize(
    "severity, severity_type, expected_cls",
    [
        (10, SeverityType.LOW, Emergency),
        (40, SeverityType.MEDIUM, Emergency),
        (70, SeverityType.HIGH, Emergency),
    ],
)
def test_pop_category_partition(
    emergency_queue, emergency_factory, severity, severity_type, expected_cls
):
    emergency_queue.push_emergency(emergency_factory(severity=severity))

    popped = emergency_queue.pop_emergency(severity_type)
    assert isinstance(popped, expected_cls)


@pytest.mark.parametrize(
    "old_sev,new_sev,matching_ids,raises",
    [
        # low -> medium, matching IDs, no raises
        (10, 50, True, False),
        # low -> medium, matching IDs, raises
        (10, 50, False, True),
        # high -> low, matching IDs, no raises
        (70, 10, True, False),
    ],
)
def test_update_emergency_category_partition(
    emergency_queue, emergency_factory, old_sev, new_sev, matching_ids, raises
):
    orig = emergency_factory(severity=old_sev)
    emergency_queue.push_emergency(orig)

    if matching_ids:
        upd = emergency_factory(
            severity=new_sev, user_uuid=orig.user_uuid, emergency_id=orig.emergency_id
        )
    else:
        upd = emergency_factory(severity=new_sev, user_uuid="diff", emergency_id=999)

    if raises:
        with pytest.raises(ValueError):
            emergency_queue.update_emergency(
                old_emergency_severity=old_sev, emergency=upd
            )
    else:
        emergency_queue.update_emergency(old_emergency_severity=old_sev, emergency=upd)
