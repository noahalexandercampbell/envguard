from __future__ import annotations

import pytest

from envguard.models import diff_env
from envguard.profile import Profile


@pytest.fixture()
def required_profile() -> Profile:
    return Profile(required=("HOST", "PORT", "DATABASE_URL"))


@pytest.fixture()
def sensitive_profile() -> Profile:
    return Profile(
        required=("DATABASE_URL", "API_KEY", "DEBUG"),
        sensitive_prefixes=("API_",),
        sensitive_patterns=(),
    )


def test_diff_detects_missing(required_profile: Profile) -> None:
    diff = diff_env({"DATABASE_URL": "sqlite://"}, required_profile)
    assert diff.missing == ("HOST", "PORT")


def test_diff_detects_extra() -> None:
    profile = Profile(required=("HOST",), allowed_extra=False)
    diff = diff_env({"HOST": "localhost", "EXTRA": "1"}, profile)
    assert diff.extra == ("EXTRA",)


def test_diff_detects_blank() -> None:
    diff = diff_env({"HOST": ""}, Profile(required=("HOST",)))
    assert diff.blank == ("HOST",)


def test_extra_when_allowed_extra_is_true() -> None:
    diff = diff_env(
        {"HOST": "localhost", "EXTRA": "1"},
        Profile(required=("HOST",), allowed_extra=True),
    )
    assert diff.extra == ()


def test_reporter_clean_state() -> None:
    from envguard.reporter import render_diff_table

    diff = diff_env({"HOST": "localhost"}, Profile(required=("HOST",)))
    message = render_diff_table(diff)
    assert message == "# All required variables are present"
    assert "localhost" not in message


def test_profile_from_dict_accepts_sensible_payload() -> None:
    from envguard.profile import Profile

    payload = {
        "required": ["API_KEY", "DATABASE_URL"],
        "allow_extra": True,
        "config": {
            "sensitive_prefixes": ["API_"],
            "sensitive_patterns": [".*_SECRET$"],
        },
    }
    profile = Profile.from_dict(payload)
    assert profile.is_sensitive("API_KEY") is True
    assert profile.is_sensitive("APP_SECRET") is True
    assert profile.is_sensitive("PORT") is False
