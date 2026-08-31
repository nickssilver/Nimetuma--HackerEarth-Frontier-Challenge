from __future__ import annotations

import argparse
import json
import sys

from nimetuma.agent import run_agent
from nimetuma.baseline import run_baseline
from nimetuma.evaluate import evaluate, render_table
from nimetuma.pack import case_by_id


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="nimetuma",
        description="Did the money actually land?",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("eval", help="Run baseline, stages, and final agent on all 10 cases")
    sub.add_parser("present", help="Judge walkthrough for the 5-minute video")
    demo = sub.add_parser("demo", help="Run one case end to end")
    demo.add_argument("case_id", help="e.g. case-02")
    demo.add_argument(
        "--stage",
        default="final",
        choices=["baseline", "screenshot_as_evidence", "till_strict", "fluent_trust", "final"],
    )
    args = parser.parse_args(argv)

    if args.cmd == "eval":
        report = evaluate()
        print(render_table(report))
        print("\nWrote results/eval.json and trajectories/<stage>/case-*.json")
        return 0

    if args.cmd == "present":
        return _present()

    case = case_by_id(args.case_id)
    trajectory = (
        run_baseline(case) if args.stage == "baseline" else run_agent(case, stage=args.stage)
    )
    print(f"{case.id}  {case.title}")
    print(f"order   {case.order_kes} KES  {case.order_item}")
    print(f"gold    {case.gold_verdict}")
    print(f"pred    {trajectory.decision.verdict}")
    print(f"why     {trajectory.decision.why}")
    print(f"seller  {trajectory.decision.seller_summary}")
    print(f"reply   {trajectory.decision.reply}")
    print(f"human   confirm before release={trajectory.decision.human_must_confirm}")
    print()
    print("trajectory:")
    print(json.dumps(trajectory.to_dict(), indent=2, ensure_ascii=False))
    return 0


def _present() -> int:
    print("NIMETUMA  Did the money actually land?")
    print("User: Amina Hassan, Amina Threads, Nairobi. Till 892341.")
    print("Bottleneck: Bro nimetuma + screenshot. Rider downstairs. Ten seconds.")
    print()

    fake = case_by_id("case-02")
    base = run_baseline(fake)
    agent = run_agent(fake)
    print("CASE 02  edited screenshot, empty till")
    print(f"  chat     {fake.chat[-1].text}")
    print(f"  baseline {base.decision.verdict:10}  {base.decision.why}")
    print(f"  agent    {agent.decision.verdict:10}  {agent.decision.why}")
    print(f"  reply    {agent.decision.reply}")
    print(f"  human    must confirm before release")
    print()

    spouse = case_by_id("case-04")
    spouse_run = run_agent(spouse)
    print("CASE 04  spouse pays, name order flipped")
    print(f"  agent    {spouse_run.decision.verdict:10}  {spouse_run.decision.why}")
    print(f"  reply    {spouse_run.decision.reply}")
    print()

    print("EVAL  same 10 cases, every stage")
    print(render_table(evaluate(write=False)))
    print()
    print("Kept: till-first verify. Removed: fluent-trust (case 10 became paid).")
    print("Hot take: Sheng made the agent easier to con. Amina still decides.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
