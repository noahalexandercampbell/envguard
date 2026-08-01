from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Profile:
    required: tuple[str, ...]
    allowed_extra: bool = False
    sensitive_prefixes: tuple[str, ...] = ()
    sensitive_patterns: tuple[re.Pattern[str], ...] = ()


    def is_sensitive(self, name: str) -> bool:
        lower = name.lower()
        for prefix in self.sensitive_prefixes:
            if lower.startswith(prefix.lower()):
                return True
        for pattern in self.sensitive_patterns:
            if pattern.search(name):
                return True
        return False

    @staticmethod
    def from_dict(payload: dict[str, object]) -> Profile:
        sensitive_prefixes: tuple[str, ...] = ()
        sensitive_patterns: tuple[re.Pattern[str], ...] = ()
        config = payload.get("config", {})
        if isinstance(config, dict):
            raw_prefixes = config.get("sensitive_prefixes", ())
            if (
                isinstance(raw_prefixes, Iterable)
                and not isinstance(raw_prefixes, (str, bytes))
            ):
                sensitive_prefixes = tuple(str(item) for item in raw_prefixes)
            raw_patterns = config.get("sensitive_patterns", ())
            if (
                isinstance(raw_patterns, Iterable)
                and not isinstance(raw_patterns, (str, bytes))
            ):
                compiled: list[re.Pattern[str]] = []
                for pattern in raw_patterns:
                    text = str(pattern)
                    try:
                        compiled.append(re.compile(text))
                    except re.error:
                        continue
                sensitive_patterns = tuple(compiled)
        required = payload.get("required", ())
        if isinstance(required, Iterable) and not isinstance(required, (str, bytes)):
            required = tuple(str(name) for name in required)
        else:
            required = (str(required),)
        allowed_extra = bool(payload.get("allow_extra", False))
        return Profile(
            required=required,
            allowed_extra=allowed_extra,
            sensitive_prefixes=sensitive_prefixes,
            sensitive_patterns=sensitive_patterns,
        )
