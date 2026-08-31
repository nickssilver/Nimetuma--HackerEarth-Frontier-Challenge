from __future__ import annotations

import re
from dataclasses import dataclass

from nimetuma.phones import normalize_ke_phone

_CODE = re.compile(r"\b([A-Z0-9]{8,12})\b")
_AMOUNT = re.compile(
    r"Kshs?\.?\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})|[0-9]+(?:\.[0-9]{2})?)",
    re.I,
)
_PHONE = re.compile(r"(\+?254\d{9}|0[17]\d{8})")
_RECEIVED = re.compile(
    r"received\s+Kshs?\.?\s*[0-9,]+(?:\.[0-9]{2})?\s+from\s+(.+?)\s+(\+?254\d{9}|0[17]\d{8})",
    re.I,
)
_PAID_TO = re.compile(r"paid to\s+(.+?)(?:\s+on\b|\.|$)", re.I)
_SENT_TO = re.compile(
    r"sent to\s+(.+?)\s+(\+?254\d{9}|0[17]\d{8})",
    re.I,
)
_REVERSAL = re.compile(r"reversal", re.I)
_DATE = re.compile(
    r"on\s+(\d{1,2}/\d{1,2}/\d{2,4})\s+at\s+(\d{1,2}:\d{2}\s*(?:AM|PM)?)",
    re.I,
)


@dataclass(frozen=True)
class ParsedSms:
    code: str | None
    amount_kes: int | None
    payer_name: str | None
    payer_phone: str | None
    destination: str | None
    is_reversal: bool
    stamp: str | None
    raw: str


def parse_mpesa_sms(text: str) -> ParsedSms:
    code_match = _CODE.search(text)
    amount_match = _AMOUNT.search(text)
    phone_match = _PHONE.search(text)
    received = _RECEIVED.search(text)
    paid_to = _PAID_TO.search(text)
    sent_to = _SENT_TO.search(text)
    date_match = _DATE.search(text)

    payer_name = None
    payer_phone = normalize_ke_phone(phone_match.group(1)) if phone_match else None
    destination = None

    if received:
        payer_name = received.group(1).strip(" .")
        payer_phone = normalize_ke_phone(received.group(2))
    elif sent_to:
        payer_name = sent_to.group(1).strip(" .")
        payer_phone = normalize_ke_phone(sent_to.group(2))

    if paid_to:
        destination = paid_to.group(1).strip(" .")

    amount = None
    if amount_match:
        amount = int(float(amount_match.group(1).replace(",", "")))

    stamp = None
    if date_match:
        stamp = f"{date_match.group(1)} {date_match.group(2).upper()}"

    return ParsedSms(
        code=code_match.group(1) if code_match else None,
        amount_kes=amount,
        payer_name=payer_name,
        payer_phone=payer_phone,
        destination=destination,
        is_reversal=bool(_REVERSAL.search(text)),
        stamp=stamp,
        raw=text,
    )


def looks_like_mpesa_sms(text: str) -> bool:
    parsed = parse_mpesa_sms(text)
    return bool(parsed.code and parsed.amount_kes is not None and "confirm" in text.lower())
