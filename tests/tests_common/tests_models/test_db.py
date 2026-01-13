import pytest
import datetime

from common.models.db import DatabaseManager
from common.models.user import User, BloodType
from common.models.emergency import Emergency
from common.models.enc_emergency import EncryptedEmergency

from tests.utils import not_raises


@pytest.fixture(autouse=True)
def reset_singleton():
    DatabaseManager._DatabaseManager__instance = None
    yield
    DatabaseManager._DatabaseManager__instance = None


@pytest.fixture
def db():
    return DatabaseManager.get_instance(":memory:")


@pytest.fixture
def sample_user():
    return User(
        uuid="user-1",
        is_rescuer=False,
        name="Mario",
        surname="Rossi",
        birthday=datetime.date(1990, 1, 1),
        blood_type=BloodType.OPOS,
        health_info_json="{}",
    )


@pytest.fixture
def rescuer_user():
    return User(
        uuid="rescuer-1",
        is_rescuer=True,
        name="Luigi",
        surname="Bianchi",
        birthday=datetime.date(1985, 5, 5),
        blood_type=BloodType.APOS,
        health_info_json="{}",
    )


@pytest.fixture
def sample_emergency(sample_user):
    return Emergency(
        emergency_id=1,
        user_uuid=sample_user.uuid,
        position=(45.0, 9.0),
        address="Via Roma",
        city="Milano",
        street_number=1,
        place_description="test place description",
        photo_b64="aaa",
        severity=3,
        resolved=False,
        emergency_type="test type",
        description="description test",
        details_json="{}",
        created_at=datetime.datetime.now(),
    )


@pytest.fixture
def sample_enc_emergency(sample_user):
    return EncryptedEmergency(
        emergency_id=1,
        user_uuid=sample_user.uuid,
        severity=3,
        routing_info_json="{}",
        blob=b"secret",
        created_at=datetime.datetime.now(),
    )


def test_get_instance_requires_path_first():
    with pytest.raises(ValueError):
        DatabaseManager.get_instance()


def test_singleton_same_instance():
    db1 = DatabaseManager.get_instance(":memory:")
    db2 = DatabaseManager.get_instance("ignored.db")
    assert db1 is db2


def test_insert_and_get_user(db, sample_user):
    db.insert_user(sample_user)

    users = db.get_users()
    assert len(users) == 1
    assert users[0].uuid == sample_user.uuid


def test_get_user_by_uuid(db, sample_user):
    db.insert_user(sample_user)

    user = db.get_user_by_uuid(sample_user.uuid)
    assert user is not None
    assert user.name == "Mario"


def test_get_user_by_uuid_not_found(db):
    assert db.get_user_by_uuid("missing") is None


def test_get_rescuers_and_rescuees(db, sample_user, rescuer_user):
    db.insert_user(sample_user)
    db.insert_user(rescuer_user)

    rescuers = db.get_rescuers()
    rescuees = db.get_rescuees()

    assert len(rescuers) == 1
    assert rescuers[0].uuid == rescuer_user.uuid

    assert len(rescuees) == 1
    assert rescuees[0].uuid == sample_user.uuid


def test_update_user(db, sample_user):
    db.insert_user(sample_user)

    sample_user.name = "Giovanni"
    db.update_user(sample_user.uuid, sample_user)

    updated = db.get_user_by_uuid(sample_user.uuid)
    assert updated.name == "Giovanni"


def test_delete_user(db, sample_user):
    db.insert_user(sample_user)
    db.delete_user(sample_user.uuid)

    assert db.get_user_by_uuid(sample_user.uuid) is None


def test_insert_emergency(db, sample_user, sample_emergency):
    db.insert_user(sample_user)

    eid = db.insert_emergency(sample_emergency)

    assert isinstance(eid, int)


def test_get_emergencies(db, sample_user, sample_emergency):
    db.insert_user(sample_user)
    db.insert_emergency(sample_emergency)

    emergencies = db.get_emergencies()
    assert len(emergencies) == 1


def test_get_emergency_by_id(db, sample_user, sample_emergency):
    db.insert_user(sample_user)
    eid = db.insert_emergency(sample_emergency)

    em = db.get_emergency_by_id(sample_user.uuid, eid)
    assert em is not None
    assert em.emergency_id == eid


def test_update_emergency(db, sample_user, sample_emergency):
    db.insert_user(sample_user)
    eid = db.insert_emergency(sample_emergency)

    sample_emergency.severity = 5
    db.update_emergency(sample_user.uuid, eid, sample_emergency)

    em = db.get_emergency_by_id(sample_user.uuid, eid)
    assert em.severity == 5


def test_delete_emergency(db, sample_user, sample_emergency):
    db.insert_user(sample_user)
    eid = db.insert_emergency(sample_emergency)

    db.delete_emergency(sample_user.uuid, eid)
    assert db.get_emergency_by_id(sample_user.uuid, eid) is None


def test_insert_encrypted_emergency(db, sample_user, sample_enc_emergency):
    db.insert_user(sample_user)

    db.insert_encrypted_emergency(sample_enc_emergency)


def test_update_encrypted_emergency(db, sample_user, sample_enc_emergency):
    db.insert_user(sample_user)
    db.insert_encrypted_emergency(sample_enc_emergency)

    sample_enc_emergency.severity = 9
    db.update_encrypted_emergency(
        sample_user.uuid,
        sample_enc_emergency.emergency_id,
        sample_enc_emergency,
    )


def test_delete_encrypted_emergency(db, sample_user, sample_enc_emergency):
    db.insert_user(sample_user)
    db.insert_encrypted_emergency(sample_enc_emergency)

    db.delete_encrypted_emergency(
        sample_user.uuid,
        sample_enc_emergency.emergency_id,
    )
