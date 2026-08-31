from __future__ import annotations

import re

from nimetuma.models import Case, Decision, ToolEvent, Trajectory
from nimetuma.parse_sms import parse_mpesa_sms

CLAIM_RE = re.compile(
    r"nimetuma|ametuma|nimetumia|i have sent|i've sent|sent\b|paid\b",
    re.I,
)

BASELINE_INSTRUCTIONS = """\
One direct prompt, no tools:
If the customer says they sent money, treat it as paid.
If a screenshot amount is present, trust it.
"""


def run_baseline(case: Case) -> Trajectory:
    chat = " ".join(message.text for message in case.chat)
    claimed = bool(CLAIM_RE.search(chat))
    events: list[ToolEvent] = [
        ToolEvent(
            thought="Read the chat the way a rushed seller would.",
            tool="read_chat",
            args={},
            observation={"claimed_sent": claimed, "has_screenshot": bool(case.screenshot_text)},
        )
    ]

    if case.screenshot_text:
        parsed = parse_mpesa_sms(case.screenshot_text)
        events.append(
            ToolEvent(
                thought="A screenshot is present. Trust the amount on it.",
                tool="read_screenshot",
                args={"text": case.screenshot_text},
                observation={"amount_kes": parsed.amount_kes, "code": parsed.code},
            )
        )
        verdict = "paid" if claimed or parsed.amount_kes else "unclear"
        why = "Customer said they paid and a screenshot amount was visible."
        code = parsed.code
    elif claimed:
        verdict = "paid"
        why = "Customer said nimetuma / sent / paid. No till check."
        code = None
    else:
        verdict = "unclear"
        why = "No clear claim in the chat."
        code = None

    decision = Decision(
        verdict=verdict,
        why=why,
        evidence=["chat-claim"] + (["screenshot"] if case.screenshot_text else []),
        reply="Ok, received. Rider can take it.",
        seller_summary="Looks paid from the chat.",
        release_recommended=verdict == "paid",
        human_must_confirm=False,
        matched_code=code,
    )
    return Trajectory(
        case_id=case.id,
        stage="baseline",
        instructions=BASELINE_INSTRUCTIONS,
        events=events,
        decision=decision,
    )
