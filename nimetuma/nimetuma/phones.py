from __future__ import annotations

import re


def normalize_ke_phone(raw: str | None) -> str | None:
    if not raw:
        return None
    digits = re.sub(r"\D", "", raw)
    if not digits:
        return None
    if digits.startswith("254") and len(digits) == 12:
        return digits
    if digits.startswith("0") and len(digits) == 10:
        return "254" + digits[1:]
    if len(digits) == 9 and digits.startswith("7"):
        return "254" + digits
    return digits


def phones_match(left: str | None, right: str | None) -> bool:
    a = normalize_ke_phone(left)
    b = normalize_ke_phone(right)
    return bool(a and b and a == b)
