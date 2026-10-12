# Upgrade the development toolchain together

This ExecPlan follows `PLANS.md` and records implementation and validation.

## Purpose / Big Picture

Contributors and CI should use current stable development tools from a consistent
lock, including uv, its build backend, pytest/plugins, checkers, formatters,
notebook and documentation tools. The candidate must retain the supported Python
3.11–3.14 matrix and exact released beartype 0.23.1 acceptance baseline.

## Progress

- [x] (2026-10-12) Verify clean main 8af59e0 and current owner instructions.
- [x] (2026-10-12) Inventory declared/locked tools and query official registries.
- [x] (2026-10-12) Create the dedicated dev-toolchain worktree and feature branch.
- [x] (2026-10-12) Commit the plan and open draft PR #60 before implementation.
- [x] (2026-10-12) Update declarations, universal lock, uv/build/workflow and hook pins.
- [x] (2026-10-12) Update current developer instructions, retaining dated evidence.
- [x] (2026-10-12) Validate runtime, checkers, floors, hooks, docs/notebook and archives.
- [x] (2026-10-12) Validate the combination with the README/coverage PR.
- [x] (2026-10-12) Record results and complete the PR for review; merge is separate.

## Surprises & Discoveries

The project and build backend restrict uv to 0.11.x; current stable uv is 0.13.0.
Its default Python selection now differs, so keep the project's explicit 3.11
pin and explicit CI interpreter matrix. Current tools include pytest 9.1.1,
Ruff 0.17.0, prek 0.5.5, mypy 2.4.0, ty 0.0.86, pyrefly 1.3.2, pyright 1.1.414,
Zensical 0.0.69 and ipykernel 7.4.0. pytest-cov, pytest-xdist and nbclient are
already at their latest stable releases. Backend versions can have newer Python
floors; the universal lock must retain compatible packages for Python 3.11.

The refreshed lock preserves NumPy 2.4.6 and JAX 0.10.2 for Python 3.11 while
selecting NumPy 2.5.4 and JAX 0.11.2 on newer supported interpreters. Ruff 0.17
mechanically migrates the existing lint-ignore syntax; no extra diagnostics were
suppressed. All 19 changed Python source/test/tool files have identical ASTs.
The updated Markdown formatter reformats 95 documentation snippets without
changing their ASTs; four long signatures needed trailing commas to keep the
existing Markdown line-length rule. Rendering and example tests pass.

GitHub action releases are verified against official tags: setup-uv v10.3.0,
upload-artifact v7.0.2 and download-artifact v8.0.2 are now pinned by exact SHA.
Checkout, Pages actions and PyPI publish were already current and retain pins.

## Decision Log

- Decision: Upgrade the full development lock while constraining beartype to
  0.23.1. Update uv 0.13.0, uv_build 0.13.x, hook versions and all active workflow
  uv pins in the same PR. Validate actual hook execution, not only configuration.
  Rationale: Tool versions, archive generation and local/hosted validation must
  agree. No global tool installation or unrelated machine changes are needed.
  Date/Author: 2026-10-12, Codex.
- Decision: Keep runtime dependency metadata, public syntax, Python support and
  compatibility-floor factors. Current development versions are distinct from
  older backend/checker versions deliberately covered by compatibility lanes.
  Retain CPU Torch source selection and do not infer CUDA support from skips.
  Date/Author: 2026-10-12, Codex.
- Decision: Preserve historical plans and benchmark reports with their original
  tool versions. Update only current commands/instructions and this plan.
  Date/Author: 2026-10-12, Codex.

## Outcomes & Retrospective

The requested development upgrades and required formatter migrations are
complete. Source, normally installed archives, minimal consumers, compatibility
floors, docs/notebook and all 36 implementation-head hosted checks pass. Both
focused PRs also pass combined validation. Python support, beartype baseline,
public behavior and the union release blocker remain unchanged. Merge,
publication, deployment, upstream contact and access changes remain separate.

## Context and Orientation

pyproject.toml contains development groups, uv settings and the uv_build range;
uv.lock resolves the supported interpreters. pytest.toml and tox.toml define
validation inputs. `.pre-commit-config.yaml` owns real hook tools/stages. All
CI, nightly and release validation share `.github/workflows/validate.yml`.
AGENTS.md, CONTRIBUTING.md and README.md state the current contributor setup.
The separate README/coverage PR adds visibility and report artifacts.

## Plan of Work

Record registry versions, then update direct development group constraints and
resolve current compatible transitive/backend versions with exact beartype.
Coordinate uv CLI, build backend, workflow and uv-pre-commit versions. Update
hook tools and plugins to current stable tags. Investigate any real regressions
from newer checkers, formatters, docs or test runners with the smallest fix;
do not suppress diagnostics or weaken consumers. Keep current instructions in
sync and add this plan to the plan index. Verify both PRs together on a separate
integration branch, preserving their independent review scopes.

## Concrete Steps

Bootstrap and record the baseline with uv 0.11.17. Install uv 0.13.0 only in a
throwaway tool environment, then use it in this worktree after updating the
required-version setting. Preserve logs under ignored build/dev-toolchain/ in
the main checkout. Run:

    uv lock --upgrade --upgrade-package beartype==0.23.1
    uv sync --locked
    uv run --locked prek install
    uv run --locked pytest tests/ --ignore=tests/test_typecheck.py -n auto
    uv run --locked pytest tests/test_typecheck.py -q
    uv run --locked prek run -a
    uv run --locked prek run actionlint -a --stage manual
    uv run --locked --only-group docs zensical build --clean
    uv run --locked --only-group docs python tools/check_docs.py
    uv run --locked python tools/check_notebook.py

Use documented tox floors and endpoint installed-archive consumers. Build the
sdist first and its wheel from that source, check distribution integrity and
record new hashes: newer uv may change archive bytes. Stage new files before
hooks and review formatting changes. Inspect final hosted checks at the reviewed
head and the combined PR validation before handing off.

## Validation and Acceptance

Current stable tools compatible with the supported interpreters are selected;
already-current tools are recorded rather than changed gratuitously. The lock,
uv/build/hook/workflow pins and current commands agree. Four checkers retain
positive, negative and native inference evidence. Runtime and all required CI
lanes, actual hooks, documentation/notebook and installed archives pass with
exact beartype 0.23.1. Compatibility floors and coverage are not lowered.

## Idempotence and Recovery

All environment/report outputs are ignored and regenerable. Feature commits
preserve main and historical evidence. Revert only this focused PR if needed;
the independent README/coverage change can remain. Never force main.

## Artifacts and Notes

Official registry inventories are retained in the main checkout's ignored build
outputs. Record before/after versions, source SHA, commands, artifacts/hashes,
failures and hosted runs here as validation completes. Union rollback remains a
release blocker regardless of tooling/CI success.

## Interfaces and Dependencies

No new checker engines or public annotation API. Use the existing validators,
locked uv toolchain, CPU backend index, hook framework and shared CI routes.

Revision, 12 October 2026: update tool declarations and coordinated uv pins;
lock resolution and behavioral validation are next.

Revision, 12 October 2026: locked runtime/checker/docs/notebook checks pass;
record necessary formatter migrations and current action pin upgrades.

Initial validation, 12 October 2026: uv sync --locked and real hook installation
pass. Commit-message stage has no file checks; normal hooks and actionlint pass.
The upgraded environment passes 1,315 runtime tests (five expected skips),
91.23% line/branch coverage and all eight four-checker suite tests. Zensical
build and rendered-structure checks pass with 95 snippets; 29 notebook cells
execute. Tox passes py311-bt0231-numpy22 and all four py313 checker floor factors,
with no floor changes. The sdist-derived wheel passes archive checks: SHA256
b41d831ecc41881e2078c28486688ceec9ef9cb9ce77087e3503617ae3fd8101;
sdist e27acf7597edfb7f4b13aed7c00883707877a2efd6f2751f7c32f7627f7e6cdd.
Fresh installed/minimal Python endpoints and combined validation follow.

## Completed review evidence

Implementation commit 743b3143ad530f807f47f89b25a1843509743f5a passes all 34
[shared CI jobs](https://github.com/beartype/bearshape/actions/runs/38228648881)
and both [proposal jobs](https://github.com/beartype/bearshape/actions/runs/38228648912).
Normally installed consumer suites pass 1,323 tests at Python 3.11.15 and 3.14.5,
including all four checkers, with five expected hardware/precision skips. Both
fresh minimal environments pass with no optional backend installed. NumPy 2.5
warns that dtype assignment in the deliberate same-object dtype-replacement
regression is deprecated; the regression passes and is retained without warning
suppression. Visual inspection of the rebuilt homepage and JAX API confirms
layout and code rendering; all 95 formatted snippets retain their original AST.

Combined validation c545e017327e06a5b6eeffa4afa6ebb72a37f1ed preserves both
implementation heads and resolves the overlapping README, changelog and plan
index. Coverage uses the updated upload-artifact pin. Normal hooks/actionlint,
1,315 runtime tests with 91.23% coverage, rendered docs structures and 1,323
normally installed consumer tests on each Python endpoint pass. Combined wheel
SHA256 is 3c2fc844f85f00bdd2fd99a27413144ec717174dd270f216b43e8b44ef6d0907;
sdist f52ada0686ec9089e648b76edb241b5200abe2c8b8c8c39bec3af45549ba8749.
Evidence lives in ignored build/dev-toolchain/ and build/maintenance-validation/
in the main checkout. This final plan update changes no validation/archive
inputs; final-head hosted checks also run automatically on push.

Revision, 12 October 2026: record completed archive, minimal, hosted and combined
validation, and mark implementation complete for review. Main is unchanged.
