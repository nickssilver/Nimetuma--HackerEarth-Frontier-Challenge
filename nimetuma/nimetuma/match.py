from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

from nimetuma.models import Case, TillRow
from nimetuma.names import names_match
from nimetuma.phones import phones_match

FRESH_WINDOW = timedelta(minutes=45)


@dataclass(frozen=True)
class MatchResult:
    verdict: Verdict
    why: str
    evidence: tuple[str, ...]
    matched_code: str | None
    used_screenshot: bool = False


def verify_case(
    case: Case,
    *,
    trust_screenshot: bool = False,
    ignore_memory: bool = False,
) -> MatchResult:
    hits = [row for row in case.till_statement if row.direction == "in"]
    reversals = {row.code for row in case.till_statement if row.direction == "reversal"}

    if trust_screenshot and case.screenshot_text:
        from nimetuma.parse_sms import parse_mpesa_sms

        fake = parse_mpesa_sms(case.screenshot_text)
        if fake.amount_kes == case.order_kes and not hits:
            return MatchResult(
                verdict="paid",
                why="Screenshot amount matches the order. Till was not checked.",
                evidence=(f"screenshot:{fake.code or 'none'}",),
                matched_code=fake.code,
                used_screenshot=True,
            )

    fresh_hits = [row for row in hits if _is_fresh(row, case)]
    amount_hits = [
        row
        for row in fresh_hits
        if row.amount_kes == case.order_kes and _destination_ok(case, row)
    ]
    reversed_hits = [row for row in amount_hits if row.code in reversals]
    if reversed_hits:
        row = reversed_hits[0]
        return MatchResult(
            verdict="unclear",
            why="A matching inbound row exists but a reversal is pending or posted.",
            evidence=(f"till:{row.code} reversed",),
            matched_code=row.code,
        )

    live_hits = [
        row
        for row in amount_hits
        if row.code not in reversals
        and _identity_ok(case, row, ignore_memory=ignore_memory)
    ]
    if live_hits:
        row = live_hits[0]
        return MatchResult(
            verdict="paid",
            why="Till row matches amount, destination, identity, and time window.",
            evidence=(f"till:{row.code} {row.amount_kes} from {row.payer_name}",),
            matched_code=row.code,
        )

    partial = [
        row
        for row in fresh_hits
        if row.code not in reversals
        and _destination_ok(case, row)
        and 0 < row.amount_kes < case.order_kes
    ]
    if partial:
        row = partial[0]
        return MatchResult(
            verdict="unclear",
            why=f"Till shows {row.amount_kes} KES against an order of {case.order_kes} KES.",
            evidence=(f"till:{row.code} partial {row.amount_kes}",),
            matched_code=row.code,
        )

    stale = [
        row
        for row in hits
        if row.amount_kes == case.order_kes and not _is_fresh(row, case)
    ]
    if stale:
        row = stale[0]
        return MatchResult(
            verdict="not_paid",
            why="A matching amount exists, but the SMS is too old for this chat.",
            evidence=(f"till:{row.code} stale at {row.at}",),
            matched_code=row.code,
        )

    if any(row.destination and row.destination != case.till for row in hits):
        return MatchResult(
            verdict="not_paid",
            why="Money moved, but not to this till.",
            evidence=tuple(f"till:{row.code} dest {row.destination}" for row in hits[:2]),
            matched_code=None,
        )

    if not hits:
        return MatchResult(
            verdict="not_paid",
            why="No inbound till row for this window. A screenshot is not evidence.",
            evidence=("till:empty",),
            matched_code=None,
        )

    return MatchResult(
        verdict="not_paid",
        why="Inbound rows exist but none match this order.",
        evidence=tuple(f"till:{row.code} {row.amount_kes}" for row in hits[:3]),
        matched_code=None,
    )


def _is_fresh(row: TillRow, case: Case) -> bool:
    row_at = datetime.fromisoformat(row.at)
    return abs(case.clock_dt() - row_at) <= FRESH_WINDOW


def _identity_ok(case: Case, row: TillRow, *, ignore_memory: bool = False) -> bool:
    claimed_phone = _claimed_phone(case)
    if phones_match(row.payer_phone, claimed_phone):
        return True
    if _name_in_chat(case, row.payer_name):
        return True
    if not ignore_memory:
        for known in case.known_payers:
            if phones_match(row.payer_phone, known.phone):
                return True
            if any(names_match(row.payer_name, name) for name in known.names):
                return True
        return names_match(row.payer_name, _claimed_name(case))
    return False


def _name_in_chat(case: Case, payer_name: str) -> bool:
    blob = " ".join(message.text for message in case.chat)
    return names_match(payer_name, blob)


def _destination_ok(case: Case, row: TillRow) -> bool:
    if not row.destination:
        return True
    return row.destination == case.till or row.destination.upper() == case.shop.upper()


def _claimed_phone(case: Case) -> str | None:
    for message in reversed(case.chat):
        from nimetuma.phones import normalize_ke_phone
        import re

        found = re.search(r"(\+?254\d{9}|0[17]\d{8})", message.text)
        if found:
            return normalize_ke_phone(found.group(1))
    return None


def _claimed_name(case: Case) -> str | None:
    for known in case.known_payers:
        if known.pays_for:
            return known.pays_for
    return None
