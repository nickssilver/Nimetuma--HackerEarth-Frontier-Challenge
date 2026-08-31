# Nimetuma

Did the money actually land?

Amina sells dresses from Nairobi on Instagram and WhatsApp. The customer says *nimetuma*, flashes a screenshot, and the rider is already downstairs. She has about ten seconds. A fake M-Pesa confirmation and an honest delayed SMS look the same.

This project is an agent that checks her till the way a trusted family member would, then drafts the reply she can send without losing the customer or the goods. It never releases the order. She does.

Kenya named the problem. The same lie exists on Venmo, UPI, Pix, and Zelle. The evaluation uses synthetic M-Pesa SMS and chats so a judge can reproduce it with no credentials and no live money.

## Who has the problem

WhatsApp and Instagram sellers, chemists, landlords, chama treasurers, shop assistants. Anyone who releases goods when a customer says they have paid.

## The bottleneck

Informal commerce runs on trust messages. Screenshots are edited, recycled, or sent to the wrong till. Regulars say *niko hurry*. Spouses pay from a different number. Fuliza reversals land after the inbound SMS. There is no staff engineer in the shop. There is a phone and a queue.

## Does the agent solve it

Yes, on a fixed pack of 10 cases that the baseline also sees.

- Screenshot text is never evidence.
- The only proof of **paid** is a matching row on the seller's own till statement.
- Identity can come from the chat or from memory of a known family payer.
- Being a regular does not fill an empty till.
- The customer reply is written in Sheng, Kiswahili, or English, matching the chat.
- A human checkpoint blocks release.

## Reproduce

```bash
cd nimetuma
python -m venv .venv
source .venv/Scripts/activate   # Windows Git Bash
pip install -e ".[dev]"
python -m nimetuma eval
pytest -q
```

Same commands work with `source .venv/bin/activate` on macOS and Linux. Docker:

```bash
docker build -t nimetuma .
docker run --rm nimetuma
```

Expected final result: **10/10 verdicts correct, 0 false paid**. Runtime is under 2 seconds. Cost is 0. No API keys.

Walkthrough of one ugly case:

```bash
python -m nimetuma present
python -m nimetuma demo case-02
python -m nimetuma demo case-02 --stage baseline
```

## Package

| Path | What it is |
| --- | --- |
| `data/eval_pack.json` | Ten synthetic cases, gold labels, till rows |
| `nimetuma/instructions.md` | Agent instructions |
| `nimetuma/agent.py` | Tool-using agent and removed experiments |
| `nimetuma/baseline.py` | One-pass "trust the chat" baseline |
| `results/eval.json` | Written by `eval` |
| `trajectories/` | One JSON trajectory per stage per case |
| `IMPROVEMENT_CHANGELOG.md` | What we tried, what the numbers did, what we kept |
| `REPRODUCTION.md` | Clean-machine guide |
| `VIDEO_SCRIPT.md` | Five-minute recording script |

Nothing in this repository existed before the competition. There are no live M-Pesa calls and no secrets.
