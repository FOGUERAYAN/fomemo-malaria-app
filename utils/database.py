"""Accès à la base SQLite et gestion sécurisée des utilisateurs (sans dépendance Streamlit)."""
import hashlib
import hmac
import os
import secrets
import sqlite3
from contextlib import contextmanager

ROLES = ("patient", "admin")
_ITERATIONS = 600_000


def db_path() -> str:
    return os.environ.get("FOMEMO_DB", "data/fomemo.db")


@contextmanager
def get_conn():
    path = db_path()
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL COLLATE NOCASE,
                role TEXT NOT NULL CHECK (role IN ('patient', 'admin')),
                age INTEGER,
                weight REAL,
                address TEXT,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (name, role)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id),
                filename TEXT,
                probability REAL NOT NULL,
                label TEXT NOT NULL CHECK (label IN ('Parasitée', 'Saine')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, _ITERATIONS)
    return f"pbkdf2_sha256${_ITERATIONS}${salt.hex()}${digest.hex()}"


def check_password(password: str, stored: str) -> bool:
    try:
        _, iterations, salt, digest = stored.split("$")
        candidate = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), int(iterations))
    except ValueError:
        return False
    return hmac.compare_digest(candidate.hex(), digest)


def create_user(name, password, role, age=None, weight=None, address=None) -> int:
    """Crée un utilisateur. Lève ValueError si les données sont invalides ou le nom déjà pris."""
    name = (name or "").strip()
    if role not in ROLES:
        raise ValueError("Rôle invalide.")
    if not name:
        raise ValueError("Le nom est obligatoire.")
    if len(password or "") < 8:
        raise ValueError("Le mot de passe doit contenir au moins 8 caractères.")
    init_db()
    try:
        with get_conn() as conn:
            cur = conn.execute(
                "INSERT INTO users (name, role, age, weight, address, password_hash) VALUES (?, ?, ?, ?, ?, ?)",
                (name, role, age, weight, address, hash_password(password)),
            )
            return cur.lastrowid
    except sqlite3.IntegrityError:
        raise ValueError("Ce nom est déjà utilisé.") from None


def verify_user(name, password, role):
    """Retourne l'utilisateur (dict sans hash) si les identifiants sont valides, sinon None."""
    init_db()
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE name = ? AND role = ?", ((name or "").strip(), role)
        ).fetchone()
    if row is None:
        # Travail factice pour limiter la différence de temps de réponse
        check_password(password or "", hash_password("x"))
        return None
    if not check_password(password or "", row["password_hash"]):
        return None
    user = dict(row)
    user.pop("password_hash")
    return user


def save_analysis(user_id: int, filename: str, probability: float, threshold: float = 0.5) -> str:
    """Enregistre une analyse et retourne le libellé ('Parasitée' ou 'Saine')."""
    label = "Parasitée" if probability > threshold else "Saine"
    init_db()
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO analyses (user_id, filename, probability, label) VALUES (?, ?, ?, ?)",
            (user_id, filename, float(probability), label),
        )
    return label


def list_analyses(user_id=None, patient_name=None, date_from=None, date_to=None):
    """Liste des analyses (plus récentes d'abord), filtrables. Les dates sont des objets date ou 'YYYY-MM-DD'."""
    init_db()
    query = (
        "SELECT a.id, u.name AS patient, a.filename, a.probability, a.label, a.created_at "
        "FROM analyses a JOIN users u ON u.id = a.user_id WHERE 1=1"
    )
    params = []
    if user_id is not None:
        query += " AND a.user_id = ?"
        params.append(user_id)
    if patient_name:
        query += " AND u.name = ?"
        params.append(patient_name)
    if date_from:
        query += " AND date(a.created_at) >= date(?)"
        params.append(str(date_from))
    if date_to:
        query += " AND date(a.created_at) <= date(?)"
        params.append(str(date_to))
    query += " ORDER BY a.created_at DESC, a.id DESC"
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(query, params).fetchall()]


def list_patient_names():
    init_db()
    with get_conn() as conn:
        rows = conn.execute("SELECT name FROM users WHERE role = 'patient' ORDER BY name").fetchall()
    return [r["name"] for r in rows]
