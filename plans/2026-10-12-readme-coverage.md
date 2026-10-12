# Make documentation and test coverage visible in the README

This ExecPlan follows `PLANS.md` and is maintained as the work progresses.

## Purpose / Big Picture

Readers should find the documentation website immediately and see the coverage
requirement beside the Python and documentation badges. CI should retain the
measured coverage for each tested platform/interpreter as downloadable reports.

## Progress

- [x] (2026-10-12) Verify clean main 8af59e0, instructions and coverage workflow.
- [x] (2026-10-12) Create the dedicated readme-coverage worktree and this plan.
- [x] (2026-10-12) Commit the plan and open draft PR #59 before implementation.
- [x] (2026-10-12) Add a prominent website link and honest coverage badge to README.
- [x] (2026-10-12) Retain JSON/XML/HTML reports from existing runtime jobs.
- [x] (2026-10-12) Validate hooks, workflow syntax, reports, archives and hosted checks.
- [x] (2026-10-12) Complete the focused PR for review; merge needs separate approval.

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

README visibility and report retention are implemented. Local runtime coverage,
all three report formats, hooks, actionlint, rendered links and archive checks
passed. All 36 implementation-head hosted checks and combined validation passed.
The focused PR is complete for review; main is unchanged. Publication, deployment
and upstream contact remain unauthorized.

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

The local runtime suite passed 1,315 tests with five expected hardware/precision
skips and 91.231566% line/branch coverage: 1,811 of 1,979 executable lines and
478 of 530 branches. JSON/XML and the 22-file HTML report agree. Normal hooks
and actionlint pass; the rendered documentation link and badge both return HTTP
200. No coverage threshold, diagnostic fixture or test collection changed.

The sdist-derived wheel passes archive checks. SHA256 values are
`151f37a7600a5161b153c50950b3dad3ad596b04484aa28942d780f929c75e08` (wheel) and
`737a06a7ddacf971849210e4abf29d66e67d724dfd760528774be47468bf0b18` (sdist).
Evidence is retained in ignored build/readme-coverage/ in the main checkout;
report files are generated under build/coverage/ in the worktree. Hosted CI
verification follows the implementation commit. The beartype 0.23.1 union
release blocker remains open.

## Interfaces and Dependencies

No new dependencies. Reuse pytest-cov, coverage and the pinned upload-artifact
action. The development-toolchain PR updates their versions separately.

Revision, 12 October 2026: implemented README visibility and report retention;
validation and final review remain pending.

Revision, 12 October 2026: local validation passed and artifact identities
recorded. Hosted and combined checks remain pending before final review.

## Completed review evidence

Implementation commit c2b861abaa419955d2348615cb4d92fb20fa1f6d passes all 34
[shared CI jobs](https://github.com/beartype/bearshape/actions/runs/38228176769)
and both [proposal jobs](https://github.com/beartype/bearshape/actions/runs/38228176665).
All eight coverage artifacts were downloaded and inspected: each contains
JSON/XML/HTML, records 91.231566% coverage, and expires seven days after creation.
The workflow artifact record ties it to the tested source SHA. Proposal checks
do not establish released native-union support.

Combined validation at c545e017327e06a5b6eeffa4afa6ebb72a37f1ed preserves this
implementation and PR #60's 743b3143ad530f807f47f89b25a1843509743f5a. It retains
the new coverage reports and updated artifact-action pin, both changelog entries
and both plans, and resolves README setup to uv 0.13.0. Normal hooks/actionlint,
1,315 runtime tests with 91.23% coverage, docs structures and normally installed
1,323 consumer tests on each Python endpoint pass. Its wheel SHA256 is
3c2fc844f85f00bdd2fd99a27413144ec717174dd270f216b43e8b44ef6d0907 and sdist
f52ada0686ec9089e648b76edb241b5200abe2c8b8c8c39bec3af45549ba8749.
Evidence remains in ignored build/maintenance-validation/ in the main checkout.
This final plan update changes no runtime, docs, workflow or archive inputs;
final-head hosted checks will also run automatically on push.

Revision, 12 October 2026: record hosted report verification and combined
validation. Implementation is complete; merging and publishing remain separate.
