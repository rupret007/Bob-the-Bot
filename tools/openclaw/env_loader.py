"""Load only Cursor credentials from regular local .env files (stdlib only)."""

from __future__ import annotations

import json
import os
import re
import shlex
import stat
from pathlib import Path
from typing import Iterable

KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
ALLOWED_KEYS = frozenset({"CURSOR_API_KEY", "CURSOR_AUTH_MODE"})


def parse_env_line(line: str) -> tuple[str, str] | None:
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    if line.lower().startswith("export "):
        line = line[7:].strip()
    if "=" not in line:
        return None
    key, _, raw_val = line.partition("=")
    key = key.strip()
    if not KEY_RE.match(key):
        return None
    raw_val = raw_val.strip()
    if not raw_val:
        return key, ""
    val = _parse_value(raw_val)
    if val is None:
        return None
    return key, val


def _parse_value(raw_val: str) -> str | None:
    try:
        parsed = json.loads(raw_val)
        if isinstance(parsed, str):
            return parsed
    except json.JSONDecodeError:
        pass
    try:
        parts = shlex.split(raw_val, posix=True)
    except ValueError:
        return None
    if len(parts) != 1:
        return None
    return parts[0]


def merge_dotenv_paths(paths: Iterable[Path], *, override: bool = False) -> list[Path]:
    loaded: list[Path] = []
    for path in paths:
        # Do not resolve symlinks before checking the file itself.
        candidate = path.expanduser().absolute()
        if _merge_file(candidate, override=override):
            loaded.append(candidate)
    return loaded


def _merge_file(path: Path, *, override: bool) -> bool:
    try:
        before = path.lstat()
        if not stat.S_ISREG(before.st_mode):
            return False
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
        with os.fdopen(os.open(path, flags), encoding="utf-8") as stream:
            opened = os.fstat(stream.fileno())
            if not stat.S_ISREG(opened.st_mode) or not os.path.samestat(before, opened):
                return False
            text = stream.read()
    except (OSError, UnicodeError):
        return False
    touched = False
    for line in text.splitlines():
        pair = parse_env_line(line)
        if not pair:
            continue
        key, value = pair
        if key not in ALLOWED_KEYS:
            continue
        if not override and key in os.environ:
            continue
        os.environ[key] = value
        touched = True
    return touched
