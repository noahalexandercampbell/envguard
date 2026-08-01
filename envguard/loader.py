from pathlib import Path
from typing import Iterable

from dotenv.main import dotenv_values


def load_env_files(paths: Iterable[Path]) -> dict[str, str]:
    env: dict[str, str] = {}
    for path in paths:
        if not path.exists():
            continue
        values = dotenv_values(path) or {}
        for key, value in values.items():
            if key is not None and value is not None:
                env[str(key)] = str(value)
    return env


def default_paths(
    root: Path | None = None,
    names: Iterable[str] | None = None,
) -> list[Path]:
    if names is None:
        names = [".env", ".env.local", ".env.ci"]
    if root is None:
        root = Path.cwd()
    return [root / name for name in names]
