from nimetuma.agent import run_agent
from nimetuma.baseline import run_baseline
from nimetuma.evaluate import evaluate
from nimetuma.pack import load_pack
from nimetuma.parse_sms import parse_mpesa_sms


def test_parser_reads_inbound_sms():
    parsed = parse_mpesa_sms(
        "TJK9Q2LM1A Confirmed. You have received Ksh3,200.00 from BRIAN OTIENO "
        "254711223344 on 31/8/26 at 2:16 PM New Till balance is Ksh41,800.00"
    )
    assert parsed.code == "TJK9Q2LM1A"
    assert parsed.amount_kes == 3200
    assert parsed.payer_phone == "254711223344"
    assert parsed.is_reversal is False


def test_final_agent_matches_gold_on_all_cases():
    for case in load_pack():
        decision = run_agent(case).decision
        assert decision.verdict == case.gold_verdict, (case.id, decision.why)
        assert decision.human_must_confirm is True


def test_baseline_is_gullible_on_empty_till():
    case = next(item for item in load_pack() if item.id == "case-02")
    decision = run_baseline(case).decision
    assert decision.verdict == "paid"


def test_fluent_trust_overrides_regular_on_empty_till():
    case = next(item for item in load_pack() if item.id == "case-10")
    decision = run_agent(case, stage="fluent_trust").decision
    assert decision.verdict == "paid"


def test_eval_final_is_perfect():
    report = evaluate(write=False)
    assert report["stages"]["final"]["correct"] == 10
    assert report["stages"]["final"]["false_paid"] == 0
    assert report["stages"]["baseline"]["accuracy"] < report["stages"]["final"]["accuracy"]
