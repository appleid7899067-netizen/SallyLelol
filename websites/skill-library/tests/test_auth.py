import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "auth.py"
spec = importlib.util.spec_from_file_location("skill_library_auth", MODULE_PATH)
auth = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = auth
spec.loader.exec_module(auth)


def valid_claims(**changes):
    claims = {
        "aud": "client-id",
        "iss": "https://accounts.google.com",
        "exp": "2000",
        "email_verified": "true",
        "sub": "stable-google-subject",
        "email": "user@example.com",
        "name": "Library User",
    }
    claims.update(changes)
    return claims


def test_google_claims_must_be_verified_and_match_client_and_issuer():
    profile = auth.validate_google_claims(valid_claims(), "client-id", now=1000)
    assert profile == {
        "google_sub": "stable-google-subject",
        "email": "user@example.com",
        "name": "Library User",
    }
    for invalid in (
        valid_claims(aud="another-client"),
        valid_claims(iss="https://evil.example"),
        valid_claims(exp="1000"),
        valid_claims(email_verified="false"),
        valid_claims(sub=""),
    ):
        with pytest.raises(ValueError):
            auth.validate_google_claims(invalid, "client-id", now=1000)


def test_oauth_state_is_short_lived_and_single_use(tmp_path):
    db = tmp_path / "identity.sqlite3"
    auth.init_db(db)
    state, verifier, nonce = auth.create_oauth_state(db, now=100)
    assert auth.consume_oauth_state(db, state, now=101) == (verifier, nonce)
    assert auth.consume_oauth_state(db, state, now=101) is None
    expired, _, _ = auth.create_oauth_state(db, now=100)
    assert auth.consume_oauth_state(db, expired, now=100 + auth.STATE_TTL_SECONDS) is None


def test_first_google_login_provisions_account_and_repeat_login_reuses_it(tmp_path):
    db = tmp_path / "identity.sqlite3"
    auth.init_db(db)
    profile = auth.validate_google_claims(valid_claims(), "client-id", now=1000)
    first_id = auth.provision_user(db, profile, now=1000)
    next_id = auth.provision_user(db, profile, now=1001)
    assert first_id == next_id


def test_sessions_are_opaque_expiring_and_revocable(tmp_path):
    db = tmp_path / "identity.sqlite3"
    auth.init_db(db)
    user_id = auth.provision_user(db, auth.validate_google_claims(valid_claims(), "client-id", now=1000), now=1000)
    session, expiry = auth.create_session(db, user_id, now=1000)
    assert auth.get_session_user(db, session, now=1001)["id"] == user_id
    assert expiry == 1000 + auth.SESSION_DAYS * 86400
    assert auth.get_session_user(db, session, now=expiry) is None
    auth.revoke_session(db, session)
    assert auth.get_session_user(db, session, now=1001) is None


def test_storage_contains_identity_only_not_chat_or_memory_tables(tmp_path):
    db = tmp_path / "identity.sqlite3"
    auth.init_db(db)
    with auth._connect(db) as conn:
        table_names = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert table_names - {"sqlite_sequence"} == {"users", "oauth_states", "sessions"}


def test_oauth_config_needs_complete_server_side_configuration(monkeypatch):
    for key in ("GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REDIRECT_URI", "SESSION_SECRET"):
        monkeypatch.delenv(key, raising=False)
    assert auth.OAuthConfig.from_env().enabled is False
    monkeypatch.setenv("GOOGLE_CLIENT_ID", "client-id")
    monkeypatch.setenv("GOOGLE_CLIENT_SECRET", "secret")
    monkeypatch.setenv("GOOGLE_REDIRECT_URI", "https://skills.example/auth/google/callback")
    monkeypatch.setenv("SESSION_SECRET", "x" * 32)
    assert auth.OAuthConfig.from_env().enabled is True
    assert auth.OAuthConfig.from_env().secure_cookie is True
