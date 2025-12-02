#!/usr/bin/env python3
"""Helper script used by the GitHub Action to run the review pipeline and emit JSON.

Reads a diff file and optional files (commits, test log, coverage before/after) and
invokes the review pipeline programmatically to avoid shell quoting issues.
"""
import argparse
import json
from autopr import reviewer, generator


def read_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--diff-file', required=True)
    parser.add_argument('--commits-file', required=False)
    parser.add_argument('--test-log', required=False)
    parser.add_argument('--coverage-before', required=False)
    parser.add_argument('--coverage-after', required=False)
    parser.add_argument('--output', required=True)

    args = parser.parse_args()

    diff = read_file(args.diff_file)
    commits = []
    if args.commits_file:
        text = read_file(args.commits_file)
        commits = [l.strip() for l in text.splitlines() if l.strip()]

    test_log = read_file(args.test_log) if args.test_log else None
    cov_before = read_file(args.coverage_before) if args.coverage_before else None
    cov_after = read_file(args.coverage_after) if args.coverage_after else None

    # produce AI review and also generate a suggested PR title/description
    review = reviewer.review_pr(diff, commits=commits, issue_text=None, test_log=test_log, coverage_before=cov_before, coverage_after=cov_after)
    pr = generator.generate_pr_from(diff, commits, None)
    res = {"pr": pr, "review": review}

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=2)


if __name__ == '__main__':
    main()
