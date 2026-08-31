# Reproduction guide

Written for a clean machine. No API keys. No network after install.

## What you need

- Python 3.11 or 3.12
- About 20 MB of disk
- The `nimetuma` folder from this submission

Optional: Docker Desktop, if you prefer not to install Python.

## Data

All inputs are in `data/eval_pack.json`. Ten cases. Each case has a chat, an optional screenshot transcript, a till statement, known payers, and a gold verdict. There is no private customer data.

## Setup

```bash
cd nimetuma
python -m venv .venv
```

Windows Git Bash:

```bash
source .venv/Scripts/activate
pip install -e ".[dev]"
```

macOS / Linux:

```bash
source .venv/bin/activate
pip install -e ".[dev]"
```

## Commands

Baseline, every failed experiment, and the final agent:

```bash
python -m nimetuma eval
```

One realistic execution:

```bash
python -m nimetuma demo case-02
```

Tests:

```bash
pytest -q
```

Docker:

```bash
docker build -t nimetuma .
docker run --rm nimetuma
```

## What to expect

`python -m nimetuma eval` prints a table like this and writes `results/eval.json`:

```
Stage                      Correct   Accuracy   False paid
-------------------------  --------  ---------  ----------
baseline                    3/10        30.0%    7/10
screenshot_as_evidence      ... 
till_strict                 ...
fluent_trust                ...
final                      10/10       100.0%    0/10
```

If the final row is not 10/10 and 0 false paid, the run did not reproduce. Open `trajectories/final/case-02.json` and compare the tool trace to the README.

Approximate runtime: 1–2 seconds on a laptop. Cost: 0.

## Versions used to produce the submitted numbers

- Python 3.12
- pytest 8
- no third-party runtime libraries

## Agent trajectories

`python -m nimetuma eval` writes `trajectories/<stage>/<case-id>.json`. Each file starts from the agent instructions, lists tool calls and observations, and ends with the verdict, the seller summary, the customer reply, and the human checkpoint.
