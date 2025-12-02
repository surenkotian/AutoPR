# AutoPR Demo Repository

This tiny demo shows how AutoPR can run on a PR to generate a PR description, run automated review (including static analysis, lint, and CI parsing), and produce a PR comment that would be posted by a GitHub Action.

What is included
- sample-project/: a small Python project with tests
- pr.diff: a sample PR diff that introduces a failing change (to demonstrate test failure + analyzer findings)
- commits.txt: example commit messages for the PR
- run_demo.py: script that runs the review runner and renders a PR comment preview
- pr_review.json: sample generated review JSON (created by the runner)
- pr_comment_preview.md: rendered markdown that mimics the GitHub Action comment

How to run locally

1. Make sure you have the venv active and the package installed (from the repo root):

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
pip install -e .
```

2. From the repo root run the demo runner which simulates the GitHub Action behavior:

```powershell
python demo/run_demo.py
```

3. Open `demo/pr_review.json` and `demo/pr_comment_preview.md` to inspect the output.
