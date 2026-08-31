from __future__ import annotations

import json
from pathlib import Path

from nimetuma.models import Case, ChatMessage, KnownPayer, TillRow

ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = ROOT / "data" / "eval_pack.json"


def load_pack(path: Path | None = None) -> list[Case]:
    payload = json.loads((path or PACK_PATH).read_text(encoding="utf-8"))
    seller = payload["seller"]
    cases: list[Case] = []
    for raw in payload["cases"]:
        cases.append(
            Case(
                id=raw["id"],
                title=raw["title"],
                seller_name=seller["name"],
                shop=seller["shop"],
                till=seller["till"],
                order_kes=raw["order_kes"],
                order_item=raw["order_item"],
                clock=raw["clock"],
                language=raw["language"],
                chat=tuple(ChatMessage(**msg) for msg in raw["chat"]),
                screenshot_text=raw.get("screenshot_text"),
                till_statement=tuple(TillRow(**row) for row in raw["till_statement"]),
                known_payers=tuple(
                    KnownPayer(
                        phone=item["phone"],
                        names=tuple(item["names"]),
                        pays_for=item["pays_for"],
                        note=item.get("note", ""),
                    )
                    for item in raw["known_payers"]
                ),
                gold_verdict=raw["gold_verdict"],
                gold_why=raw["gold_why"],
            )
        )
    return cases


def case_by_id(case_id: str, path: Path | None = None) -> Case:
    for case in load_pack(path):
        if case.id == case_id:
            return case
    raise KeyError(case_id)
