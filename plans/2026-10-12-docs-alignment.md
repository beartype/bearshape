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
- [x] (2026-10-12) Commit the plan and open draft PR #58 before implementation.
- [x] (2026-10-12) Inventory every tracked Markdown artifact, notebook narrative,
  public docstring and relevant configuration; audit links and current claims.
- [x] (2026-10-12) Correct installation, usage and support guidance; close
  contributor workflow gaps and distinguish current status from historical evidence.
- [x] (2026-10-12) Execute relevant examples and notebook, build and inspect
  rendered docs, check local links and verify installed archive metadata.
- [x] (2026-10-12) Normal and real pre-push hooks pass. Hosted baseline
  validation and both proposal endpoints pass on the implementation head.
- [x] (2026-10-12) Record coverage, outcomes, artifact hashes and hosted
  validation; prepare PR #58 for review. Merge approval remains separate.

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

The documentation corrections are implemented in PR #58. Local example,
checker, notebook, rendered-site, link and minimal-consumer validation passes.
The source changes affect docstrings only; runtime behavior, dependency metadata
and the unresolved union release blocker are unchanged. Normal/pre-push hooks
and all 36 hosted checks pass at implementation head 910bad8. Final audit
record updates are checked again on the PR head before handoff. This describes
the implementation review before merge approval; the subsequent review and
approval record follows below. No publication or deployment is authorized.

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


## Audit register — 12 October 2026

The final inventory contains 81 tracked Markdown entries (including the
`CLAUDE.md` symlink), plus the notebook, public source docstrings, badges,
HTML overrides and executable workflow/configuration references.

- Root guidance (six entries): README, AGENTS, CLAUDE, CONTRIBUTING, PLANS and
  CHANGELOG now agree on the unpublished candidate, support matrix, release
  blocker, current commands and review responsibilities. The symlink still
  resolves to AGENTS. The changelog preserves authorship and historical work.
- User/maintainer website (25 Markdown files): checked every guide and API page
  against current exports, converters, memo ownership, dimension/Tree handling
  and runtime/static consumers. Installation, Like typing, custom dtype/scalar
  factories, check/check_context, standalone examples and release commands were
  corrected. The unchanged CuPy, OpTree, claw and framework pages remain aligned
  with their tested boundaries. Added an explicit composition limitation page
  and its navigation entry. Current handoff evidence is separated from older
  reports instead of silently rewriting their test results.
- Plans (42 entries): the index lists all 40 earlier dated plans. Their version,
  command, pending-review and performance claims were checked for stale active
  guidance. Each now explicitly identifies its contents as dated evidence;
  #56/#57 have appended merge/cleanup closeouts. This plan owns the docs audit.
  Historical implementation narratives and original results were preserved.
- Tool/proposal/evidence guidance (seven Markdown files): validator commands
  agree with their parsers, tox factors and workflows; upstream integration is
  clearly unshipped, with isolation-stage counts distinguished from final
  optimization validation. Benchmark reports retain source identities, raw
  samples and original interpreter/dependency versions.
- Contributor PR template (one Markdown file): prompts for the concrete change,
  plan/dependency links, validation evidence, docs and compatibility effects.
- Notebook/public docstrings: use public DtypeSpec construction, correct native
  static annotations, accurate scalar-casting/memo behavior and runnable import
  context. Corrected Dimension doctest representations. No executable library
  AST changed after stripping docstrings.
- Other artifacts: the active SVG badge already says Python 3.11–3.14. Removed
  the unreferenced PNG saying 3.10–3.14. Repaired the theme's generated 404 page
  skip-to-content anchor with a minimal template override. Package/workflow
  metadata and lock remain unchanged; the current docs navigation includes
  the composition guide.

### Evidence and checks

Primary-source checks used [PyPI](https://pypi.org/project/bearshape/) for the
0.0.1 upload date (29 May 2026),
[the GitHub release](https://github.com/beartype/bearshape/releases/tag/v0.0.1)
for the original release date (31 March 2026, retained in CHANGELOG), and
[CuPy installation](https://docs.cupy.dev/en/stable/install.html) for CUDA-specific
package selection. These are dated facts, not an assertion that current main is
published.

On Python 3.11.15 with uv 0.11.17 and exact beartype 0.23.1:

- Executed 81 CPU user-guide Python blocks, checking intended exception calls.
  Nine contextual snippets depend on a containing application/static fixture;
  their matching existing consumer/claw fixtures were checked separately. Three
  CuPy snippets were not executed without CUDA. The known union reproducer is
  deliberately documented as a defect, not counted as passing. Two corrected
  positive examples were called explicitly: padded arrays have the advertised
  result shape, and Tree processing returns its input.
- `pytest tests/test_examples.py tests/test_factory_aliases.py tests/test_claw.py
  -q`: six passed. `pytest tests/test_typecheck.py -q`: eight passed across all
  four engines. Dimension doctests: three attempted, zero failures.
- Zensical build and `tools/check_docs.py` passed: expected rendered tables,
  admonitions and favicon; 95 Python 3.11 snippets parsed. Parsing and execution
  totals intentionally differ. `tools/check_notebook.py`: all 29 code cells
  executed. `tox list` confirms the documented environment names exist.
- Checked 237 local Markdown file links and 2,561 local HTML references,
  including 1,298 anchors, with no unresolved targets. The HTML check maps the
  configured `/bearshape/` site prefix to the build root. Inspected home,
  installation, composition and handoff pages in a local browser.
- Built the sdist first, then its wheel; `tools/check_distribution.py` passed.
  The documented fresh minimal-consumer recipe passed with no optional backend
  installed or imported. Archive hashes are recorded below after final build.
- Runtime-source AST comparison with main a475c9b confirms docstring-only source
  changes. Local logs and inventory are retained under ignored
  `build/docs-alignment/` in the main checkout.

Revision note — 2026-10-12: Record completed artifact audit, corrected user and
contributor contracts, preserved historical evidence and local validation.


### Final implementation validation and artifact identities

The documentation implementation is 910bad807584476b0930ca76fc41457a8184361b,
following 871d42737f64fe0a8c4241d69e704d22b81cb5f9 and the initial plan commit.
All 34 [CI jobs](https://github.com/beartype/bearshape/actions/runs/38221049041)
and both [proposal endpoints](https://github.com/beartype/bearshape/actions/runs/38221048953)
passed on that implementation, including installed consumers, compatibility
floors, four checker engines, both notebook endpoints and docs. Real pre-push
runtime/checker hooks passed. Eight additional standalone public help examples
were executed on CPU; the CuPy help example still requires CUDA. An AST
comparison of all nine changed library modules confirms docstrings only.

The final audit record restores the original GitHub release date in CHANGELOG
instead of substituting the later PyPI upload date. The final archive pair
includes that correction; normal hooks, archive integrity and the hosted
matrix are checked on the final PR head. The final run links and exact head are
recorded in the PR validation description rather than a self-referential commit
hash in this file.

- Wheel SHA256: `4617bf301f9183f47fc1f7115cdd69afced2e345a2841a587e4729ef56ed5f39`.
- Source archive SHA256: `448f8b1b8fa36d4c525b36b0fa9693ab7af17af692ba2e0ce07cf35adce17453`.

These identify documentation-audit artifacts, not release approval. The review
baseline is main a475c9b; supported upstream union integration and the release
runbook's external prerequisites remain open. No runtime optimization or public
API change is included in this audit.

Revision note — 2026-10-12: Close out local and hosted documentation validation,
record final archive identities and preserve the original release chronology.


### Owner-approved review and merge — 12 October 2026

The owner subsequently requested review followed by merge into main. Review of
468fdabd30402044f15c3405ae893413c6cf7d4c found no blocking issues: public guidance
matches the current APIs and validation routes; historical evidence is retained;
all nine library edits are docstrings only; the unaccepted upstream proposal and
released-dependency union defect remain explicit. All 36 hosted checks passed
on that reviewed head. The plan/index now record approval rather than retaining
a pending-review statement.

Merge with a merge commit, preserve every reviewed commit, verify main and
archive only the clean merged worktree after saving useful ignored evidence.
The final PR check status and merge SHA are recorded on
[PR #58](https://github.com/beartype/bearshape/pull/58); local review/main-check
results belong in ignored `build/docs-merge-closeout/` in the main checkout.
This approval does not authorize publication, deployment or upstream contact.

Revision note — 2026-10-12: Record the owner's review-and-merge approval and
review outcome without changing release readiness or the upstream boundary.
