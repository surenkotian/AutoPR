#!/usr/bin/env python3
"""Run a local demo of PR review using the pr_review_runner script.

This script:
- runs tests on the base sample-project
- applies the demo PR diff temporarily to sample-project
- runs tests on the PR version (capturing failures)
- calls the pr_review_runner to produce a review JSON
- renders the PR comment preview Markdown
"""
import subprocess
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "demo" / "sample-project"
PR_DIFF = ROOT / "demo" / "prs" / "pr.diff"
COMMITS = ROOT / "demo" / "prs" / "commits.txt"
OUT_JSON = ROOT / "demo" / "pr_review.json"
OUT_MD = ROOT / "demo" / "pr_comment_preview.md"


def run_pytest(cwd: Path, out_file: Path):
    print(f"Running pytest in {cwd} -> {out_file}")
    with out_file.open('w', encoding='utf-8') as f:
        subprocess.run([shutil.which('python') or 'python', '-m', 'pytest', '-q'], cwd=str(cwd), stdout=f, stderr=subprocess.STDOUT)


def apply_diff_to_file(diff_file: Path, target_file: Path):
    # read diff file that contains added lines with leading +
    added_lines = []
    for ln in diff_file.read_text(encoding='utf-8').splitlines():
        if ln.startswith('+') and not ln.startswith('+++'):
            added_lines.append(ln[1:])

    # write the added lines as replacement content for target (demo simplification)
    target_file.write_text('\n'.join(added_lines), encoding='utf-8')


def render_markdown_from_json(js: dict) -> str:
    md = []
    md.append('# AutoPR — Review Summary (demo)')
    md.append('')

    pr = js.get('pr', {})
    review = js.get('review', {})

    if pr:
        md.append('## 📝 Generated PR')
        md.append(f"**Title:** {pr.get('title', '')}\n")
        md.append('<details><summary>Generated PR description</summary>\n')
        if pr.get('what_changed'):
            md.append(f"**What changed:** {pr.get('what_changed')}\n")
        if pr.get('why'):
            md.append(f"**Why:** {pr.get('why')}\n")
        if pr.get('files_impacted'):
            md.append(f"**Files:** {', '.join(pr.get('files_impacted'))}\n")
        if pr.get('tests'):
            md.append(f"**Tests:** {pr.get('tests')}\n")
        if pr.get('risk_level'):
            md.append(f"**Risk level:** {pr.get('risk_level')}\n")
        md.append('</details>\n')

    if review:
        md.append('## ✅ AI Review Summary')
        if review.get('summary'):
            md.append(review.get('summary'))

        if review.get('findings'):
            md.append('\n### Findings')
            for f in review['findings'][:25]:
                md.append(f"- **{f.get('type', 'unknown')}** ({f.get('severity') or 'info'}): {f.get('message')}")

    # Tests
    if review.get('_tests'):
        t = review['_tests']
        md.append('\n## 🧪 Tests')
        md.append(f"Passed: {t.get('passed')} • Failed: {t.get('failed')} • Errors: {t.get('errors')} • Skipped: {t.get('skipped')}")

    # Coverage
    if review.get('_coverage'):
        c = review['_coverage']
        md.append('\n## 📊 Coverage')
        md.append(f"Before: {c.get('before')}% • After: {c.get('after')}% • Δ: {c.get('delta')}%")

    # Issue alignment
    if review.get('_issue_alignment'):
        ia = review['_issue_alignment']
        md.append('\n## 🎯 Issue alignment')
        md.append(f"Score: {ia.get('score')} • Matched: {', '.join(ia.get('matched', []))}")

    return '\n'.join(md)


def main():
    # ensure sample project tests pass initially
    run_pytest(SAMPLE, ROOT / 'demo' / 'base_test.log')

    # backup file
    target = SAMPLE / 'src' / 'sample.py'
    backup = SAMPLE / 'src' / 'sample.py.bak'
    shutil.copy(str(target), str(backup))

    print('Applying PR diff...')
    apply_diff_to_file(PR_DIFF, target)

    try:
        run_pytest(SAMPLE, ROOT / 'demo' / 'pr_test.log')

        # run the review runner to generate JSON
        runner = ROOT / '.github' / 'scripts' / 'pr_review_runner.py'
        cmd = [shutil.which('python') or 'python', str(runner), '--diff-file', str(PR_DIFF), '--commits-file', str(COMMITS), '--test-log', str(ROOT / 'demo' / 'pr_test.log'), '--output', str(OUT_JSON)]
        print('Running review runner:', ' '.join(cmd))
        subprocess.run(cmd, check=True)

        # create markdown preview
        data = json.loads(OUT_JSON.read_text(encoding='utf-8'))
        # runner now returns { pr: {...}, review: {...} }
        pr = data.get('pr', {})
        review = data.get('review', {})
        md = render_markdown_from_json({'pr': pr, 'review': review})
        OUT_MD.write_text(md, encoding='utf-8')
        print('Demo outputs written to', OUT_JSON, OUT_MD)

    finally:
        # restore backup
        shutil.move(str(backup), str(target))


if __name__ == '__main__':
    main()
