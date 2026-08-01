from __future__ import annotations

from dataclasses import dataclass, field

from envguard.profile import Profile


@dataclass(frozen=True)
class EnvDiff:
    missing: tuple[str, ...]
    extra: tuple[str, ...]
    blank: tuple[str, ...]
    profile: Profile = field(repr=False)


def diff_env(env: dict[str, str], profile: Profile) -> EnvDiff:
    missing = tuple(name for name in profile.required if name not in env)
    extras = tuple(name for name in env if name not in profile.required)
    blank = tuple(name for name in env if env[name] == "")
    if not profile.allowed_extra:
        extra = tuple(sorted(extras))
    else:
        extra = ()
    return EnvDiff(missing=missing, extra=extra, blank=blank, profile=profile)
