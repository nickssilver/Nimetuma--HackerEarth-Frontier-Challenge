from __future__ import annotations

from nimetuma.models import Case, Decision
from nimetuma.match import MatchResult


def draft_decision(case: Case, match: MatchResult) -> Decision:
    reply = _reply(case, match)
    seller_summary = _seller_summary(case, match)
    return Decision(
        verdict=match.verdict,
        why=match.why,
        evidence=list(match.evidence),
        reply=reply,
        seller_summary=seller_summary,
        release_recommended=match.verdict == "paid",
        human_must_confirm=True,
        matched_code=match.matched_code,
    )


def _seller_summary(case: Case, match: MatchResult) -> str:
    if match.verdict == "paid":
        return (
            f"Till 892341 received {case.order_kes} KES for {case.order_item}. "
            f"Code {match.matched_code}. You still confirm before the rider leaves."
        )
    if match.verdict == "unclear":
        return (
            f"Do not release {case.order_item} yet. {match.why} "
            "Wait for the rest, or for the reversal to settle."
        )
    return (
        f"Do not release {case.order_item}. {match.why} "
        "If they paid another till, they need the M-Pesa SMS, not a screenshot."
    )


def _reply(case: Case, match: MatchResult) -> str:
    lang = case.language
    if match.verdict == "paid":
        if lang == "kiswahili":
            return (
                f"Nimeona {case.order_kes} kwenye till, code {match.matched_code}. "
                "Napeana kwa rider sasa."
            )
        if lang == "english":
            return (
                f"Got the {case.order_kes} on the till, code {match.matched_code}. "
                "Handing it to the rider now."
            )
        return (
            f"Nimeona {case.order_kes} kwa till, code {match.matched_code}. "
            "Rider anachukua sasa."
        )
    if match.verdict == "unclear":
        if "partial" in match.why.lower() or "against an order" in match.why.lower():
            if lang == "kiswahili":
                return (
                    f"Nimeona {match.matched_code} lakini ni kidogo kuliko {case.order_kes}. "
                    "Tuma salio kisha nitoe bidhaa."
                )
            if lang == "english":
                return (
                    f"I can see {match.matched_code}, but it is short of {case.order_kes}. "
                    "Send the balance and I will release."
                )
            return (
                f"Nimeona {match.matched_code} but sio full {case.order_kes}. "
                "Tuma balance ndio nitoe."
            )
        if lang == "kiswahili":
            return (
                "Kuna SMS ya till na pingamizi. Ngoja kidogo, "
                "nisitoe bidhaa hadi iwe wazi."
            )
        if lang == "english":
            return (
                "A till SMS came in and then a reversal. "
                "I will hold the order until it settles."
            )
        return (
            "Kuna reversal kwenye till. Ngoja iwe clear, "
            "sijatoa bidhaa bado."
        )
    if lang == "kiswahili":
        return (
            f"Bado sijaona {case.order_kes} kwenye till {case.till}. "
            "Tuma SMS halisi ya M-Pesa, si screenshot."
        )
    if lang == "english":
        return (
            f"The {case.order_kes} has not landed on till {case.till} yet. "
            "Send the actual M-Pesa SMS, not a screenshot."
        )
    return (
        f"Bado sijaona {case.order_kes} kwa till {case.till}. "
        "Tuma message ya M-Pesa, si screenshot."
    )
