# HackerEarth form — four fields only

This matches the Create submission modal: Title, Description, Video URL, Source Code.

Deadline: Monday 31 Aug 2026, 18:00 UTC (21:00 Nairobi).

Use **Save as Draft** until the video URL is a real public or unlisted link. Then Submit.

---

## 1. Title

```
Nimetuma — Did the money actually land?
```

## 2. Description

Paste this into the editor. After paste: select the four questions and the two result lines and make them bold if you want.

```
Nimetuma is an agent for Kenyan WhatsApp and Instagram sellers who have about ten seconds to decide whether to release goods after a customer says nimetuma and sends an M-Pesa screenshot.

Who has this problem?
Sellers, chemists, landlords, and chama treasurers. Amina Hassan of Amina Threads is the named user. Till 892341.

What bottleneck makes it worth solving?
Informal commerce runs on trust messages. A fake confirmation, a recycled SMS, a spouse paying from another number, a lookalike till, a partial send, and a reversal all look like “I have paid” in the chat. Kenya named the problem. The same lie exists on Venmo, UPI, Pix, and Zelle.

Does the agent solve it well?
It never treats a screenshot or the word nimetuma as proof. The only evidence of paid is a matching row on the seller’s own till statement (amount, destination, freshness, identity, including known family payers). It drafts a reply in Sheng, Kiswahili, or English. It does not release goods. A human checkpoint blocks that.

Can another person reproduce the result?
Yes. The zip is self-contained. No API keys. No live M-Pesa. Synthetic chats and till rows only.

python -m venv .venv
source .venv/Scripts/activate
pip install -e ".[dev]"
python -m nimetuma eval

On macOS or Linux use source .venv/bin/activate. Docker: docker build -t nimetuma . && docker run --rm nimetuma. Expected result: 10/10 correct, 0 false paid. Runtime under 2 seconds. Cost 0. Full steps in REPRODUCTION.md.

Measured improvement (same 10 cases every stage)
Baseline: 3/10 correct, 7 false paid
Final agent: 10/10 correct, 0 false paid

Improvement changelog is IMPROVEMENT_CHANGELOG.md. The change that mattered most was refusing screenshots as evidence. The experiment we removed was fluent-trust: Sheng plus a known regular made case 10 “paid” on an empty till.

Hot take: language comfort made the agent easier to con. Amina still decides.

Inside the zip
• Full solution code and agent instructions (nimetuma/instructions.md)
• Improvement changelog
• Reproduction guide
• Agent trajectories for baseline, failed experiments, and the final agent (start at trajectories/final/case-02.json)
• Video script: python -m nimetuma present
```

## 3. Video URL

Required. Record now:

```
cd nimetuma
python -m nimetuma present
```

Upload unlisted to YouTube (or a public Google Drive link that opens without a login). Paste that https URL here.

Do not Submit until this is a real link. A placeholder will get the submission rejected or ignored.

## 4. Source Code

Click Upload File and choose:

```
C:\Users\workstation\Desktop\Development\Self\Frontier Engineering\submission\Nimetuma-micro1-Frontier-Engineering-2026.zip
```

183 KB. Under the 50 MB limit.

## Then

Save as Draft if the video is not up yet. Submit only when all four fields are real.
