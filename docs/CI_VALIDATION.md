# CI Validation and Test Parsing

This module contains utilities to help summarize CI runs and validate PR test impacts.

Features
- Parse pytest logs (counts of passed/failed/test failures) — `autopr.ci_parser.parse_pytest_output`
- Parse and compare coverage summaries — `autopr.coverage_utils.parse_coverage_summary` and `compare_coverage`
- Simple issue alignment check to determine whether a PR's diff/commits likely address an issue — `autopr.issue_validator.simple_issue_alignment`

CLI commands
- `ci-parse` — parse pytest logs
- `coverage-compare` — compare before/after coverage summaries
- `validate-issue` — check similarity between issue text and PR diff/commits

Integration
- These utilities are integrated into the review orchestration and can be passed via CLI or programmatically to `reviewer.review_pr` to surface test/coverage/issue validation details.
