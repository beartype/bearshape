# Make documentation and test coverage visible in the README

This ExecPlan follows `PLANS.md` and is maintained as the work progresses.

## Purpose / Big Picture

Readers should find the documentation website immediately and see the coverage
requirement beside the Python and documentation badges. CI should retain the
measured coverage for each tested platform/interpreter as downloadable reports.

## Progress

- [x] (2026-10-12) Verify clean main 8af59e0, instructions and coverage workflow.
- [x] (2026-10-12) Create the dedicated readme-coverage worktree and this plan.
- [ ] Commit this plan and open a draft PR before implementation.
- [ ] Add a prominent website link and honest coverage badge to README.
- [ ] Retain JSON/XML/HTML coverage reports from the existing runtime jobs.
- [ ] Validate hooks, workflow syntax, reports, archives and hosted checks.
- [ ] Present the focused PR for review; merge needs its own approval.

## Surprises & Discoveries

README already contains a Docs badge linking to the website, but no prominent
text link. Runtime CI already measures branch-inclusive coverage and enforces
90 percent. It prints the result but does not retain coverage report artifacts.

## Decision Log

- Decision: Show the enforced 90-percent coverage floor in the badge, explicitly
  labelled as a coverage gate, and link to CI. Retain actual measurements in
  named JSON/XML/HTML artifacts for every CPU runtime lane.
  Rationale: Avoid a stale percentage or an unconfigured external service. The
  badge makes the existing guarantee visible; reports provide exact values,
  source revision, uncovered lines and platform differences.
  Date/Author: 2026-10-12, Codex.
- Decision: Keep the existing threshold, test collection and expected hardware
  skips. No runtime, support-matrix or publication changes.
  Date/Author: 2026-10-12, Codex.

## Outcomes & Retrospective

Implementation pending. Publication, deployment and upstream contact remain
unauthorized. The separate development-toolchain PR is independent of this work.

## Context and Orientation

README.md is the public package description. The website is
https://beartype.github.io/bearshape/. `.github/workflows/validate.yml` owns the
shared runtime jobs and their `--cov-fail-under=90` gate. `pyproject.toml` enables
branch coverage. CONTRIBUTING.md documents how to run and interpret checks.

## Plan of Work

Add a normal Documentation text link near the README introduction and a coverage
badge beside its existing badges. Explain that the displayed value is the CI
floor. Extend the existing pytest command to emit coverage.json, coverage.xml
and htmlcov/; upload them with platform/Python-specific names and a short
retention period. Keep the existing upload action pin and read-only permissions.
Document local reproduction and report scope in CONTRIBUTING.md/tools/README.md.

## Concrete Steps

Work in the readme-coverage worktree on codex/readme-coverage. With the current
locked uv 0.11.17 toolchain:

    uv sync --locked
    uv run --locked prek install
    uv run --locked pytest tests/ --ignore=tests/test_typecheck.py -n auto \
      --cov=bearshape --cov-branch --cov-report=term-missing:skip-covered \
      --cov-report=json:build/coverage/coverage.json \
      --cov-report=xml:build/coverage/coverage.xml \
      --cov-report=html:build/coverage/htmlcov --cov-fail-under=90
    uv run --locked prek run -a
    uv run --locked prek run actionlint -a --stage manual

Inspect all generated report formats, verify the README badge/link, and build
and check the matching sdist/wheel. Push through actual pre-push hooks and inspect
all hosted checks on the final PR head. Preserve logs in ignored
build/readme-coverage/ in the main checkout.

## Validation and Acceptance

The README has an obvious website link and a coverage-gate badge. The badge
agrees with the unchanged CI threshold. Actual runtime reports contain branch
measurements and package file coverage, and are retained as CI artifacts.
Existing required checks remain successful; CPU results do not establish CUDA
coverage. No secret, service account, publishing branch or deployment is needed.

## Idempotence and Recovery

Reports and build outputs are regenerable and ignored. Main stays clean and
unchanged while the PR is reviewed. Revert this focused PR if needed; do not
revert the unrelated development-toolchain work.

## Artifacts and Notes

Record source SHA, report summary, archive hashes and hosted run URLs here after
validation. The beartype 0.23.1 union release blocker remains open.

## Interfaces and Dependencies

No new dependencies. Reuse pytest-cov, coverage and the pinned upload-artifact
action. The development-toolchain PR updates their versions separately.
