Contributing
============

Please follow the project guidelines when contributing. Use branches per feature and open a PR.

Pre-commit hooks
-----------------
This repository uses `pre-commit` to run linters and formatters automatically before commits.

To set it up locally:

```bash
python -m pip install -r requirements-dev.txt
pre-commit install
pre-commit run --all-files
```

The `pre-commit` configuration includes hooks for `ruff` (auto-fix) and `black`.

If you add or update dependencies, regenerate `requirements.lock`:

```bash
.venv/bin/python -m pip freeze > requirements.lock
git add requirements.lock
git commit -m "chore: update requirements.lock"
```
