# Prepare invariant shape traversal once per annotation

## Purpose / Big Picture

Complete the remaining invariant preparation suggested by the audit, following
merged lazy-scope and Tree leaf optimizations. Array annotations have immutable
shape specifications, but every input, return and Tree leaf scans them for a
variadic dimension and repeatedly slices the same specification. Prepare this
layout when constructing a validator. Actual shapes, memo bindings and Value
arguments remain live per invocation; no array, frame, memo or scope is cached.

This focused PR starts at main 28e8858 and is independent of dtype PR #56.
Validate each separately, then their combination in a temporary integration
checkout. Preserve every reviewed commit; no merge or publication is implicit.

## Progress

- [x] Read the current contract, profile and merged optimization evidence.
- [x] Create this plan before implementation.
- [x] Open focused PR and add relevant semantic guards.
- [x] Prepare shape traversal without changing order, errors or rollback.
- [x] Validate source and installed consumers, then matched benchmarks.
- [x] Record evidence and submit a concrete review result.

## Surprises & Discoveries

The 100-leaf profile performs 200,000 identical variadic searches per 1,000
input/return calls. Dtype calculation is a separate hotspot handled by #56.
The earlier PR already avoids repeated Tree context discovery and keeps at
least 202 snapshots per 100-leaf input/return; preserve that guarantee.

## Decision Log

- 2026-10-11: Prepare only immutable annotation layout, including fixed rank or
  variadic prefix/suffix. Share the same checking implementation with the
  existing internal check_shape entry point. Avoid duplicated dimension logic,
  global shape caches and generated checking code.
- Keep the existing check order: rank, prefix, suffix, variadic middle. Symbolic
  expressions can depend on earlier bindings, and diagnostics expose that order.

## Outcomes & Retrospective

Implementation and local validation are complete; the focused PR remains open for review. Baseline beartype 0.23.1 still requires supported
upstream composition integration before release; this optimization cannot
remove that external prerequisite.

## Context and Orientation

`src/bearshape/_shape.py` owns immutable DimSpec values and matching.
`_ArrayChecker` and `_ArrayLikeChecker` in `_array_types.py` currently call
check_shape on each value. Tree delegates to these validators. Existing shape,
array, Tree, Value, rollback, lifetime and upstream composition tests cover the
contract and must continue passing without relaxation.

## Plan of Work

Introduce one private prepared shape checker, owned by each array validator.
Move the current traversal into it while retaining dimension-matching helpers.
The compatibility function check_shape delegates to the same implementation.
Add guards for reuse across independent memos/Value scopes and stable failure
order. Extend matched benchmarks to include multi-axis and variadic shapes,
construction and native controls. Use normal installs, identical scripts and
pinned inputs, recording unfavorable cases as well as improvements.

## Concrete Steps

Run locked uv 0.11.17 sync and install hooks. Exercise focused regressions,
then `uv run --locked pytest tests/ --ignore=tests/test_typecheck.py -n auto`,
`uv run --locked pytest tests/test_typecheck.py -q` and normal hooks.
Validate the combined final wheel with normally installed Python 3.11/3.14
consumers, fresh minimal environments and the complete local upstream proposal.
Do not replace the released baseline in the lock or count skips as support.

## Validation and Acceptance

All current shapes and error text remain valid, including empty/anonymous,
fixed, named, arithmetic, broadcast and variadic dimensions. Repeated calls
must re-read mutable shape metadata and Value arguments and release owned
objects. Tree visits every leaf and preserves rollback snapshots. Installed
benchmarks must demonstrate useful savings against current main without a
flaky CI timing threshold or a universal zero-overhead claim.

## Idempotence and Recovery

Main remains unchanged. Branch codex/shape-preparation holds this independent
change; a temporary integration branch will combine approved work for testing.
Revert any unhelpful optimization. Benchmark outputs are regenerable; preserve
raw evidence and final artifact identities before cleanup.

## Artifacts and Notes

Start: main 28e885837e61705d3d3295463874c3e0acf35ca8. Earlier scope/Tree evidence
lives in tools/evidence/2026-10-11-audit-performance; it is historical and does
not establish the benefit of this new optimization.

## Interfaces and Dependencies

Keep check_shape's signature and return contract. No public API or dependency
changes. A private checker accepts each actual shape, ShapeMemo and optional
Value scope; its persistent fields contain only annotation DimSpec tuples and
rank/layout integers. Reuse existing _check_fixed_dims and _check_variadic.

Revision note — 2026-10-11: Created before implementation to keep shape
preparation separate from dtype normalization.


## Completed validation and review evidence

The final runtime heads are dtype `6ae31a27fd5a2a95991c29433585cd342f47a1a0`
and shape `4c0a65be3ae737c13d82944b1c0592cd343cbe10`. The isolated combined
head `e5eddd6aa0cab07a35e1ed4b25c00b2f6dade5cf` preserves both histories.
Each focused implementation passed runtime tests and all four checker suites;
both PRs passed all 36 hosted checks at those implementation heads. Later
documentation commits rerun normal hooks and hosted checks without changing
runtime artifacts.

The combined wheel passes 1,323 normally installed baseline tests and 1,450
proposal tests per endpoint (CPython 3.11.15 and 3.14.5), including all four
consumer checkers, 69 composition cases and 58 upstream protocol/scope/mixin
cases. The original union probe passes with the proposal. Source coverage is
91.23%. Minimal installed consumers pass without optional backends. Documentation
build/render checks and 95 snippets pass. Five local skips cover absent CuPy
and platform-specific extended precision, not union behavior.

Matched 5,000-call, nine-repeat measurements compare main, each PR independently,
and their combination with released and proposal dependencies. They run
sequentially on the same local host with identical normally installed inputs,
reversing variant order on 3.14. Cold initialization uses 13 fresh subprocesses;
root-only and ordinary beartype controls are recorded separately. The complete
report, hashes, methods and raw samples are in PR #56 under
`tools/evidence/2026-10-11-remaining-optimization/`. Local commands, logs and
exact archives are preserved in the main checkout's ignored
`build/remaining-optimization/`.

The dtype implementation retains only known builtin class identities and names,
not dtype instances or checked values. Review caught custom metaclass hashing
and root-only string overhead; both have focused guards and are resolved in the
final head. Shape preparation retains only annotation layout and preserves
prefix/suffix/middle ordering, live Value scopes and every Tree snapshot.
An extra upstream lookup cache was rejected after isolated measurements showed
only about 20 ns best-case savings on 3.11 and a slowdown on 3.14, before cache
maintenance costs. The upstream patch series is unchanged.

Main remains at 28e8858. The old validation worktree was removed only after
checking its conflict resolutions and parent reachability and preserving its
complete Git history plus generated documentation. The new validation checkout
is relevant to these still-open PRs. No publication, upstream contact or
repository administration has occurred. The published dependency still lacks
full union rollback; approved release controls and exact-wheel CUDA evidence
remain external release prerequisites.

Revision note — 2026-10-11: Record the finished implementation, protocol guards,
matched performance tradeoffs and final installed validation; keep merge state
and release readiness distinct.
