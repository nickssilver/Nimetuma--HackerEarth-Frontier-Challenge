from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from nimetuma.agent import run_agent
from nimetuma.baseline import run_baseline
from nimetuma.models import Case, Trajectory
from nimetuma.pack import load_pack

STAGES = (
    "baseline",
    "screenshot_as_evidence",
    "till_strict",
    "fluent_trust",
    "final",
)

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
TRAJECTORIES = ROOT / "trajectories"


def run_stage(case: Case, stage: str) -> Trajectory:
    if stage == "baseline":
        return run_baseline(case)
    return run_agent(case, stage=stage)


def evaluate(
    stages: tuple[str, ...] = STAGES,
    write: bool = True,
) -> dict:
    cases = load_pack()
    report: dict = {"stages": {}, "cases": [case.id for case in cases]}
    for stage in stages:
        rows = []
        for case in cases:
            trajectory = run_stage(case, stage)
            correct = trajectory.decision.verdict == case.gold_verdict
            false_paid = (
                trajectory.decision.verdict == "paid" and case.gold_verdict != "paid"
            )
            rows.append(
                {
                    "case_id": case.id,
                    "title": case.title,
                    "gold": case.gold_verdict,
                    "pred": trajectory.decision.verdict,
                    "correct": correct,
                    "false_paid": false_paid,
                    "why": trajectory.decision.why,
                    "reply": trajectory.decision.reply,
                }
            )
            if write:
                dest = TRAJECTORIES / stage
                dest.mkdir(parents=True, exist_ok=True)
                (dest / f"{case.id}.json").write_text(
                    json.dumps(trajectory.to_dict(), indent=2, ensure_ascii=False),
                    encoding="utf-8",
                )
        correct_n = sum(1 for row in rows if row["correct"])
        false_paid_n = sum(1 for row in rows if row["false_paid"])
        report["stages"][stage] = {
            "correct": correct_n,
            "n": len(rows),
            "accuracy": round(correct_n / len(rows), 3),
            "false_paid": false_paid_n,
            "false_paid_rate": round(false_paid_n / len(rows), 3),
            "rows": rows,
        }
    if write:
        RESULTS.mkdir(parents=True, exist_ok=True)
        (RESULTS / "eval.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return report


def render_table(report: dict) -> str:
    lines = [
        "Stage                      Correct   Accuracy   False paid",
        "-------------------------  --------  ---------  ----------",
    ]
    for stage, payload in report["stages"].items():
        lines.append(
            f"{stage:<25}  {payload['correct']:>2}/{payload['n']:<4}  "
            f"{payload['accuracy']:>7.1%}   {payload['false_paid']:>2}/{payload['n']}"
        )
    lines.append("")
    final = report["stages"].get("final")
    if final:
        lines.append("Final agent vs gold")
        lines.append("Case       Gold        Pred        OK  Title")
        lines.append("---------  ----------  ----------  --  -----")
        for row in final["rows"]:
            mark = "Y" if row["correct"] else "N"
            lines.append(
                f"{row['case_id']:<9}  {row['gold']:<10}  {row['pred']:<10}  {mark}   {row['title']}"
            )
    return "\n".join(lines)


def confusion(stage_payload: dict) -> Counter:
    counts: Counter = Counter()
    for row in stage_payload["rows"]:
        counts[(row["gold"], row["pred"])] += 1
    return counts
