# Video script · under 5 minutes

One take. Terminal only. Unlisted YouTube when you are done.

## Record this

```bash
python -m nimetuma present
```

That prints the problem, case 02 (baseline vs agent), case 04 (spouse), the eval table, and the hot take.

If you want the longer version, use the beats below.

## 0:00–0:40  Problem and baseline

Say: Amina sells on WhatsApp. The customer writes *Bro nimetuma* and sends a screenshot. The rider is downstairs.

```bash
python -m nimetuma demo case-02 --stage baseline
```

Point at `pred paid`. The till is empty. The baseline believed the screenshot.

## 0:40–2:20  One realistic execution

```bash
python -m nimetuma demo case-02
```

Walk `read_case` → `query_till` (empty) → `verify` (screenshot ignored) → `draft_reply` → `human_checkpoint`.

Read the reply: *Bado sijaona 4500 kwa till 892341. Tuma message ya M-Pesa, si screenshot.*

```bash
python -m nimetuma demo case-04
```

Mary Wanjiru pays for James. Name order is flipped. Verdict is paid. Human still confirms.

## 2:20–3:40  Comparison

```bash
python -m nimetuma eval
```

Baseline 3/10 and 7 false paid. Final 10/10 and zero false paid.

## 3:40–4:30  Changelog

The change that mattered most: refusing screenshots as evidence.

The experiment we removed: fluent-trust. Sheng and a known regular made case 10 paid on an empty till.

## 4:30–5:00  Close

No live M-Pesa. No keys. `python -m nimetuma eval` on a clean machine. Amina still decides.

## Upload

YouTube unlisted. Paste the URL into the HackerEarth **Video link** field before you publish.
