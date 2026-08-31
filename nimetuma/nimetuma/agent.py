from __future__ import annotations

from pathlib import Path

from nimetuma.match import verify_case
from nimetuma.models import Case, ToolEvent, Trajectory
from nimetuma.parse_sms import parse_mpesa_sms
from nimetuma.reply import draft_decision

INSTRUCTIONS = Path(__file__).with_name("instructions.md").read_text(encoding="utf-8")

FLUENT_TRUST_INSTRUCTIONS = """\
If the customer writes fluent Sheng or Kiswahili and sounds like a regular,
treat nimetuma as paid even when the till is quiet. Neighbors do not lie.
"""


def run_agent(case: Case, stage: str = "final") -> Trajectory:
    if stage == "screenshot_as_evidence":
        return _screenshot_stage(case)
    if stage == "till_strict":
        return _till_stage(case, require_known=False, require_phone=True)
    if stage == "fluent_trust":
        return _fluent_trust_stage(case)
    return _final_stage(case)


def _final_stage(case: Case) -> Trajectory:
    events: list[ToolEvent] = []
    events.append(
        ToolEvent(
            thought="Read the order, chat, and clock. Ignore the screenshot as proof.",
            tool="read_case",
            args={"case_id": case.id},
            observation={
                "order_kes": case.order_kes,
                "item": case.order_item,
                "till": case.till,
                "language": case.language,
                "chat": [message.text for message in case.chat],
                "screenshot_present": bool(case.screenshot_text),
            },
        )
    )
    events.append(
        ToolEvent(
            thought="Query the seller till. Screenshot text is not a till row.",
            tool="query_till",
            args={"till": case.till, "window_minutes": 45},
            observation=[
                {
                    "code": row.code,
                    "amount_kes": row.amount_kes,
                    "at": row.at,
                    "direction": row.direction,
                    "payer": row.payer_name,
                    "phone": row.payer_phone,
                }
                for row in case.till_statement
            ],
        )
    )
    events.append(
        ToolEvent(
            thought="Check whether this number is a known family or regular payer.",
            tool="lookup_known_payer",
            args={},
            observation=[
                {
                    "phone": known.phone,
                    "names": list(known.names),
                    "pays_for": known.pays_for,
                    "note": known.note,
                }
                for known in case.known_payers
            ],
        )
    )
    match = verify_case(case, trust_screenshot=False)
    events.append(
        ToolEvent(
            thought="Verify amount, destination, identity, freshness, and reversals.",
            tool="verify",
            args={"trust_screenshot": False},
            observation={
                "verdict": match.verdict,
                "why": match.why,
                "evidence": list(match.evidence),
            },
        )
    )
    decision = draft_decision(case, match)
    events.append(
        ToolEvent(
            thought="Draft a reply in the customer's register. Do not accuse on unclear.",
            tool="draft_reply",
            args={"language": case.language},
            observation={"reply": decision.reply, "seller_summary": decision.seller_summary},
        )
    )
    events.append(
        ToolEvent(
            thought="Seller releases goods. The agent does not.",
            tool="human_checkpoint",
            args={"action": "release_goods"},
            observation={
                "blocked": True,
                "release_recommended": decision.release_recommended,
                "human_must_confirm": True,
            },
        )
    )
    return Trajectory(
        case_id=case.id,
        stage="final",
        instructions=INSTRUCTIONS,
        events=events,
        decision=decision,
    )


def _screenshot_stage(case: Case) -> Trajectory:
    match = verify_case(case, trust_screenshot=True)
    decision = draft_decision(case, match)
    events = [
        ToolEvent(
            thought="Parse the screenshot as if it were a till SMS.",
            tool="parse_screenshot",
            args={},
            observation=parse_mpesa_sms(case.screenshot_text).raw
            if case.screenshot_text
            else None,
        ),
        ToolEvent(
            thought="If the screenshot amount matches the order, call it paid.",
            tool="verify",
            args={"trust_screenshot": True},
            observation={"verdict": match.verdict, "why": match.why},
        ),
    ]
    return Trajectory(
        case_id=case.id,
        stage="screenshot_as_evidence",
        instructions="Treat a parsed screenshot as till evidence.",
        events=events,
        decision=decision,
    )


def _till_stage(case: Case, require_known: bool, require_phone: bool) -> Trajectory:
    match = verify_case(case, ignore_memory=True)
    events = [
        ToolEvent(
            thought="Accept identity only from this chat. Ignore family memory.",
            tool="verify",
            args={"ignore_memory": True},
            observation={"verdict": match.verdict, "why": match.why},
        )
    ]
    decision = draft_decision(case, match)
    return Trajectory(
        case_id=case.id,
        stage="till_strict",
        instructions="Till rows only. No family-memory identity.",
        events=events,
        decision=decision,
    )


def _fluent_trust_stage(case: Case) -> Trajectory:
    from nimetuma.match import MatchResult

    match = verify_case(case)
    fluent = case.language in {"sheng", "kiswahili"}
    claimed = any(
        word in " ".join(message.text for message in case.chat).lower()
        for word in ("nimetuma", "ametuma", "hurry")
    )
    if match.verdict == "not_paid" and fluent and claimed and case.known_payers:
        match = MatchResult(
            verdict="paid",
            why="Fluent regular. Trusted the chat over the empty till.",
            evidence=("fluent-trust",),
            matched_code=None,
        )
    decision = draft_decision(case, match)
    return Trajectory(
        case_id=case.id,
        stage="fluent_trust",
        instructions=FLUENT_TRUST_INSTRUCTIONS,
        events=[
            ToolEvent(
                thought="Customer sounds local and known. Maybe the till SMS is just late.",
                tool="trust_register",
                args={"language": case.language},
                observation={"overrode_till": match.why.startswith("Fluent")},
            )
        ],
        decision=decision,
    )
