# Contributing

Work happens on branches. Main stays green.

1. Open an issue first if the change is more than a typo.
2. Branch from `main`: `git checkout -b fix/short-name`
3. Keep the eval honest. Same 10 cases. Do not tune gold labels to hide a miss.
4. Open a pull request. The template asks for eval + pytest.

```bash
cd nimetuma
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m nimetuma eval
pytest -q
```

A PR that drops below 10/10 or adds a false paid needs a written reason in the description.
