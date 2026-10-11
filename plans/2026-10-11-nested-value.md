# Preserve scope in nested Value arithmetic


This living ExecPlan follows `PLANS.md` and M2 of `plans/2026-10-11-release-readiness.md`. The program plan supplies the full release contract; this focused change is stacked on baseline PR #39.

## Purpose / Big Picture


`N + (Value("size") + 1)` currently becomes a dimension-only expression and fails to resolve size. Recognize `_ValueExpr` in `src/bearshape/_dimensions.py::_binop` so all derived runtime expressions retain scope. Preserve all operators, operand orders and public annotations. Add nested arithmetic, unary, attribute and parameter/return positive and negative cases in `tests/test_dimensions.py` and `tests/test_numpy.py`.

## Progress


- [x] (2026-10-11) Reproduced the defect during the whole-library audit; created the focused branch and plan.
- [ ] Commit plan and open draft PR before implementation.
- [ ] Add a failing behavioral regression, implement the surgical fix and update CHANGELOG.
- [ ] Run focused existing tests, real hooks and four-checker consumers; record the before/after evidence.

## Surprises & Discoveries


The October audit reproducer demonstrates this defect on both earlier rc0 and released beartype 0.23.1. It is independent of the native composite-union upstream blocker.

## Decision Log


Decision: Preserve public syntax, successful behavior and useful errors; fix only this demonstrated correctness defect. Rationale: the owner requested every audit finding be addressed in focused PRs on Python 3.11+ and beartype 0.23.1. Author/date: owner/Codex, 2026-10-11.

## Outcomes & Retrospective


Implementation and validation pending. This PR does not authorize merging or publishing and does not claim to fix native union transactions.

## Context and Orientation


The implementation and test locations are named above. Array and tree leaves use invocation-local `ShapeMemo` state from `src/bearshape/_memo.py`; failed leaf checks and diagnostic formatting must restore state. Root imports must remain free of NumPy/JAX/Torch/CuPy/optree. The baseline is `codex/python311-beartype0231`, with all four static consumer engines retained.

## Plan of Work


First add a regression exercising the audited invalid behavior and run it against unchanged source. Save the failure under the main checkout's ignored `build/release-2026-10-11/evidence/`. Make the smallest source change described above, retaining the surrounding validation and state lifetime contract. Add positive/negative neighboring cases where the new branch needs proof, then run the focused modules. Update CHANGELOG and this plan, stage new files before hooks, review formatter changes and commit/push the concrete result.

## Concrete Steps


From this worktree with uv 0.11.17 on PATH:

    uv sync --locked
    uv run --locked prek install
    uv run --locked pytest tests/test_dimensions.py tests/test_numpy.py -n 0
    uv run --locked pytest tests/test_typecheck.py -q
    uv run --locked prek run -a

Real pre-push hooks also run the complete runtime and four-checker suites. Archive, platform and CUDA evidence will be refreshed on the combined integration branch.

## Validation and Acceptance


The audited reproducer fails before and passes after the source fix. Neighboring valid forms remain valid and wrong shapes/types still reject with useful errors. Existing memo rollback/lifetime and static inference tests remain effective. No xfail, suppression, lowered coverage or optional-backend import is introduced. Detailed scope and acceptance cases are stated in Purpose above.

## Idempotence and Recovery


Use the matching isolated worktree/environment. Do not modify main or existing unmerged PR branches. Keep evidence outside disposable worktrees. Do not publish, deploy or send maintainer messages. Re-running the tests is safe.

## Artifacts and Notes


Original audit evidence is `/Users/ale/Code/bearshape/build/audit-2026-10-11/`. New logs belong under `build/release-2026-10-11/evidence/` in that same main checkout. Append meaningful results and source identities after implementation.

## Interfaces and Dependencies


No new runtime dependency or public API. Retain Python 3.11–3.14, exact tested beartype 0.23.1, existing backend semantics and the four supported checker engines. Dimensions remain runtime constraints rather than static shape proofs.

Revision note — 2026-10-11: Created the focused regression/fix plan before implementation.
