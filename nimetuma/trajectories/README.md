# Agent trajectories

Each file is one case at one stage. Start at `instructions`, walk `events` (thought → tool → observation), then read `decision`.

```
trajectories/
  baseline/                 trust the chat
  screenshot_as_evidence/   parse screenshot as till
  till_strict/              till only, no family memory
  fluent_trust/             removed experiment
  final/                    submitted agent
```

Read these first:

- `final/case-02.json` — fake screenshot, empty till, human checkpoint
- `final/case-04.json` — spouse memory, name order flipped
- `fluent_trust/case-10.json` — the experiment we removed
- `baseline/case-02.json` — same case, gullible baseline

Regenerate:

```bash
python -m nimetuma eval
```
