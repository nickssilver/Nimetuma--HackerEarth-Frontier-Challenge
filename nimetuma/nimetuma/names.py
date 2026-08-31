from __future__ import annotations

import re

_KEEP = re.compile(r"[^A-Z\s]")


def tokens(name: str | None) -> list[str]:
    if not name:
        return []
    cleaned = _KEEP.sub(" ", name.upper())
    return [part for part in cleaned.split() if part and part not in {"THE", "OF"}]


def names_match(left: str | None, right: str | None) -> bool:
    a = tokens(left)
    b = tokens(right)
    if not a or not b:
        return False
    if a == b or sorted(a) == sorted(b):
        return True
    if _initials_match(a, b) or _initials_match(b, a):
        return True
    overlap = set(a) & set(b)
    return len(overlap) >= 2


def _initials_match(short: list[str], full: list[str]) -> bool:
    if len(short) < 2 or len(full) < 2:
        return False
    last_ok = short[-1] == full[-1] or short[-1] == full[0]
    first_ok = len(short[0]) == 1 and short[0] == full[0][:1]
    return last_ok and first_ok
