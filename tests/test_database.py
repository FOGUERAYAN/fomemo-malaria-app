import pytest

from utils import database as db


@pytest.fixture(autouse=True)
def tmp_db(tmp_path, monkeypatch):
    monkeypatch.setenv("FOMEMO_DB", str(tmp_path / "test.db"))


def test_create_and_verify_user():
    db.create_user("Alice", "motdepasse1", "patient", age=30)
    user = db.verify_user("alice", "motdepasse1", "patient")  # insensible à la casse
    assert user["name"] == "Alice" and "password_hash" not in user


def test_wrong_password_or_role_rejected():
    db.create_user("Alice", "motdepasse1", "patient")
    assert db.verify_user("Alice", "faux", "patient") is None
    assert db.verify_user("Alice", "motdepasse1", "admin") is None
    assert db.verify_user("Inconnu", "motdepasse1", "patient") is None


def test_duplicate_and_validation():
    db.create_user("Alice", "motdepasse1", "patient")
    with pytest.raises(ValueError):
        db.create_user("alice", "motdepasse1", "patient")
    with pytest.raises(ValueError):
        db.create_user("Bob", "court", "patient")
    with pytest.raises(ValueError):
        db.create_user("", "motdepasse1", "patient")
    with pytest.raises(ValueError):
        db.create_user("Bob", "motdepasse1", "root")


def test_password_is_hashed_with_salt():
    h1, h2 = db.hash_password("secret123"), db.hash_password("secret123")
    assert h1 != h2 and "secret123" not in h1
    assert db.check_password("secret123", h1)


def test_analyses_saved_and_filtered():
    alice = db.create_user("Alice", "motdepasse1", "patient")
    bob = db.create_user("Bob", "motdepasse1", "patient")
    assert db.save_analysis(alice, "a.png", 0.9) == "Parasitée"
    assert db.save_analysis(alice, "b.png", 0.1) == "Saine"
    db.save_analysis(bob, "c.png", 0.7)

    assert len(db.list_analyses()) == 3
    assert len(db.list_analyses(user_id=alice)) == 2
    assert [r["patient"] for r in db.list_analyses(patient_name="Bob")] == ["Bob"]
    assert db.list_analyses(date_from="2999-01-01") == []
    assert db.list_patient_names() == ["Alice", "Bob"]
