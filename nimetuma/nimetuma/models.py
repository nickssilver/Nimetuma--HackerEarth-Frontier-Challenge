from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Literal

Verdict = Literal["paid", "not_paid", "unclear"]


def parse_clock(value: str) -> datetime:
    return datetime.fromisoformat(value)


@dataclass(frozen=True)
class ChatMessage:
    sender: str
    text: str
    at: str


@dataclass(frozen=True)
class TillRow:
    code: str
    sms: str
    at: str
    direction: Literal["in", "reversal"]
    amount_kes: int
    payer_name: str
    payer_phone: str
    destination: str


@dataclass(frozen=True)
class KnownPayer:
    phone: str
    names: tuple[str, ...]
    pays_for: str
    note: str = ""


@dataclass(frozen=True)
class Case:
    id: str
    title: str
    seller_name: str
    shop: str
    till: str
    order_kes: int
    order_item: str
    clock: str
    language: str
    chat: tuple[ChatMessage, ...]
    screenshot_text: str | None
    till_statement: tuple[TillRow, ...]
    known_payers: tuple[KnownPayer, ...]
    gold_verdict: Verdict
    gold_why: str

    def clock_dt(self) -> datetime:
        return parse_clock(self.clock)


@dataclass
class ToolEvent:
    thought: str
    tool: str
    args: dict[str, Any]
    observation: Any


@dataclass
class Decision:
    verdict: Verdict
    why: str
    evidence: list[str] = field(default_factory=list)
    reply: str = ""
    seller_summary: str = ""
    release_recommended: bool = False
    human_must_confirm: bool = True
    matched_code: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Trajectory:
    case_id: str
    stage: str
    instructions: str
    events: list[ToolEvent]
    decision: Decision

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "stage": self.stage,
            "instructions": self.instructions,
            "events": [asdict(event) for event in self.events],
            "decision": self.decision.to_dict(),
        }
