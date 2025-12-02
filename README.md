# AutoPR — AI-powered Pull Request Generator & Reviewer

AutoPR automates the repetitive parts of pull requests for teams: it writes concise PR titles & descriptions, validates CI/tests, runs deterministic static and lint checks, and provides an AI-assisted review summary. This repository is an MVP scaffold for that functionality.

What this repo provides
- A FastAPI backend with /generate and /review endpoints (with a pluggable LLM provider; a local stub is included)
- A developer-friendly CLI `pr-ai` (generate, review, analyze, ci-parse, coverage-compare, validate-issue)
- AST-based static analyzer for Python and deterministic lint checks
- Tools to parse CI output and compare coverage to detect regressions
- A GitHub Actions workflow + helper scripts to review PRs and post a polished comment
- Demo scaffolding you can deploy to GitHub to demonstrate the feature end-to-end

Quickstart
1. Create a virtual environment and install requirements:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

2. Make the package importable (recommended)

Install in editable mode so the `autopr` package is on your environment path. This makes `uvicorn autopr.main:app` work without needing to set PYTHONPATH each time.

```powershell
pip install -e .
```

3. Run the API locally:

```powershell
uvicorn autopr.main:app --reload --port 8000
```

3. Try the endpoints with curl or the CLI:

```powershell
curl -X POST http://127.0.0.1:8000/generate -H "Content-Type: application/json" -d '{"diff":"+ added line", "commits": ["fix: add helper"], "issue":"#123"}'
pr-ai gen --diff "+ added line" --commits "fix: add helper" --issue "#123"
```

API docs
--------

After starting the server the OpenAPI UI is available at:

- http://127.0.0.1:8000/docs — Interactive docs (Swagger UI)
- http://127.0.0.1:8000/openapi.json — Raw OpenAPI JSON spec

The docs include the request/response schemas we use for /generate and /review, and you can try the endpoints directly from the UI to see example outputs (the default "stub" provider returns deterministic mock results).

Example curl responses (stub provider)
------------------------------------

```powershell
curl -X POST http://127.0.0.1:8000/generate -H "Content-Type: application/json" -d '{"diff":"+ added line", "commits": ["fix: add helper"], "issue":"#123"}'
# -> returns JSON object for title, what_changed, why, files_impacted, tests, risk_level, rollback_plan

curl -X POST http://127.0.0.1:8000/review -H "Content-Type: application/json" -d '{"diff":"print(\"debug\")\n# TODO: remove"}'
# -> returns JSON object with summary, findings (array), and confidence
```

CI / Test validation & utilities
--------------------------------

This project includes tools to parse CI/test output and compare coverage so PR validation can be automated.

CLI examples (after activating venv):

```powershell
# Parse a pytest/CI log file
.\.venv\Scripts\python.exe -m autopr.cli ci-parse --log path\to\pytest.log

# Compare coverage summaries (before/after)
.\.venv\Scripts\python.exe -m autopr.cli coverage-compare --before cov_before.txt --after cov_after.txt

# Validate whether diff/commits align with an issue text
.\.venv\Scripts\python.exe -m autopr.cli validate-issue --issue "Fix login" --diff "+def login(user, pass): ..." --commits "fix: handle tokens"
```

Static analyzer (Python)
------------------------

This project includes a lightweight AST-based static analyzer for Python snippets/diffs. It is run automatically by the `POST /review` endpoint and is available via the CLI `pr-ai analyze`.

Examples:

```powershell
# Run analyzer on a diff using CLI
python -m autopr.cli analyze --diff "+def foo():\n+  print('debug')\n+  # TODO: remove" --lang python

# Call the review endpoint (will include static analysis findings alongside AI findings)
curl -X POST http://127.0.0.1:8000/review -H "Content-Type: application/json" -d '{"diff": "+def foo():\n+  print(\"debug\")\n+  # TODO: remove"}'
```

See `docs/PRD.md` for the full product requirements and MVP scope used to build this scaffold.

Using a real LLM provider
------------------------

This project supports three provider modes: `openai`, `anthropic`, and `stub`.

- Set the environment variable `AUTOPR_PROVIDER` to `openai` or `anthropic` to use a real provider.
- Provide the appropriate environment variables containing API keys:
	- `OPENAI_API_KEY` and optionally `OPENAI_MODEL` (e.g. gpt-4o)
	- `ANTHROPIC_API_KEY` and optionally `ANTHROPIC_MODEL` (e.g. claude-2)
- A `.env.example` file is included to show the expected variable names. Do not commit real API keys to your repo.

Local development (safety)
-------------------------
The default `stub` provider is safe for development and offline test runs. When testing providers in CI, always mock network calls so secrets are not required.

Quick alternative: run directly using PYTHONPATH
------------------------------------------------
If you prefer not to install the package, you can run uvicorn with the `src` path on PYTHONPATH so the `autopr` package is importable without installation:

```powershell
$env:PYTHONPATH = "src"; uvicorn autopr.main:app --reload --port 8000
```


License: MIT
