# Align user and contributor documentation with merged main

This ExecPlan is maintained under `PLANS.md`. It covers documentation and the
checks needed to establish that the documented workflows and examples work.

## Purpose / Big Picture

A user should be able to install the intended revision, choose a backend,
write valid annotations, and understand current limitations without reading
maintainer history. An external contributor should be able to create a focused
change, run the appropriate checks and submit it through the repository's
review framework. Dated experiments remain evidence for their original sources;
current instructions must describe merged main and the unpublished candidate.

## Progress

- [x] (2026-10-12) Verify clean main a475c9b and read repository instructions,
  current release contract, contributor commands and recent optimization plans.
- [x] (2026-10-12) Create a dedicated docs-alignment worktree and this plan.
- [ ] Commit the plan and open a focused PR before implementation.
- [ ] Inventory and audit every tracked Markdown artifact, notebook narrative,
  user-facing template and relevant configuration against code/tests/workflows.
- [ ] Correct user installation, usage and support guidance; close contributor
  workflow gaps and distinguish current status from historical evidence.
- [ ] Execute relevant examples and notebook, build and inspect rendered docs,
  check local links and normal hooks, and verify installed archive metadata.
- [ ] Record coverage, outcomes and hosted validation; present the PR for review.

## Surprises & Discoveries

The initial pass finds installation commands which imply that PyPI contains the
unpublished 0.1.0rc1 candidate; landing pages omit the maintained Pyrefly engine;
and the handoff and optimization plans still describe merged PRs #56/#57 as
open. Current main is a475c9b5376601eb39c9e0641f16f62d56fed979 and preserves both
reviewed histories. These are documentation defects, not API changes.

## Decision Log

The owner requested a complete docs/artifact audit on 12 October 2026, including
README, AGENTS and contributor guidance. This authorizes documentation fixes
and validation in a focused PR. It does not authorize merge, publication,
deployment, external messages or administration for this new scope.

Keep public syntax, Python 3.11–3.14 support, four checkers and exact beartype
0.23.1 validation. The existing union rollback defect remains a release blocker.
Do not modify runtime behavior or use documentation changes to narrow the
accepted contract. Use current source and tests as evidence; flag any actual
runtime discrepancy separately. Preserve dated results and append explicit
status updates where a completed plan would otherwise mislead a reader.

## Outcomes & Retrospective

Audit in progress. No implementation changes or support claims are complete yet.

## Context and Orientation

`README.md` and `docs/getting-started/` are the entry points. `docs/features/`
and `docs/api/` describe annotations exported from `src/bearshape/`; tests and
`tests/typing/` establish runtime and static consumer support. `CONTRIBUTING.md`
owns the human workflow, `AGENTS.md` and its `CLAUDE.md` symlink own agent rules,
`PLANS.md` defines execution plans, and `tools/README.md` describes validators.
`docs/maintainers/production-readiness.md` and `releasing.md` describe current
release prerequisites and historical evidence. `plans/` and `tools/evidence/`
contain dated records; `tools/upstream/` contains a separate unshipped upstream
proposal. `zensical.toml`, `.github/workflows/`, `pyproject.toml`, `tox.toml` and
hook configuration are the executable source of workflow facts.

## Plan of Work

Start with a complete tracked-file inventory and record a disposition for every
document family. Read user guides and API tables against exports, converters,
decorators, dimension/Tree behavior and real consumer tests. Check notebook
narrative, rendered landing-page text, docstrings, badges, links and workflow
instructions. Verify public distribution/version facts against primary sources.

Update README and installation pages so the current development candidate is
not confused with a published release. Explain the open composition defect,
backend installation and runtime/static boundaries at the right entry points.
Fix runnable examples if they contain placeholders or unsupported assumptions.
Complete contributor setup, change scope, regression expectations, validation
selection and review/merge responsibilities without duplicating agent policy.
Refresh the current handoff and completed-plan status while retaining historical
source identities, hashes and results. Keep the audit register in this plan.

## Concrete Steps

Use `/Users/ale/.codex/worktrees/docs-alignment/bearshape` for edits on
`codex/docs-alignment`. Use uv 0.11.17 with the repository lock. Run from that
worktree:

    uv sync --locked
    uv run --locked prek install
    uv run --locked pytest tests/test_examples.py -q
    uv run --locked --only-group docs zensical build --clean
    uv run --locked --only-group docs python tools/check_docs.py
    uv run --locked python tools/check_notebook.py
    uv run --locked prek run -a

If the checker guidance or fixtures change, run the full four-engine harness:

    uv run --locked pytest tests/test_typecheck.py -q

Build the source archive first and then the wheel from it, following the
contributor guide. Validate the matching archive pair with
`tools/check_distribution.py`. Inspect rendered changed pages in a local
browser, and use read-only checks to verify local documentation links. Stage
new files before hooks; inspect formatting changes before committing. Push the
focused PR and check hosted validation at its final reviewed head.

## Validation and Acceptance

All tracked documentation receives an explicit audited disposition. Current
user guidance must agree with exports, runtime tests, checker consumers and
installation metadata. Contributor commands must name existing groups, tools
and tox factors. Documentation builds without new broken local links; runnable
examples and notebook cells pass; normal hooks pass. Historical checks/skips
must not be presented as current backend evidence. Publication remains blocked
by supported union integration and the existing release prerequisites.

## Idempotence and Recovery

Docs builds and validation outputs are regenerable. Keep logs and the inventory
under ignored `build/docs-alignment/` in the main checkout, outside the temporary
worktree. Commit only reviewed documentation and any necessary example/checker
validation changes. Revert focused commits if wording is incorrect. Main stays
unchanged until this PR receives approval.

## Artifacts and Notes

The initial main commit is a475c9b5376601eb39c9e0641f16f62d56fed979. Its merged
optimization wheel and source archive are recorded in the preceding plans and
`tools/evidence/2026-10-11-remaining-optimization/README.md`. Documentation edits
will change archive hashes; do not claim byte-identical artifacts after them.

## Interfaces and Dependencies

No public runtime API, package version, dependency range or checker support
change. Reuse existing documentation tools and the shared validation workflow.
Do not add a parallel documentation framework, speculative features or broad
runtime cleanup.

Revision note — 2026-10-12: Initial plan before implementation for the owner's
complete documentation-alignment request.
