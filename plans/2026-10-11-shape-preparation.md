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
- [ ] Open focused PR and add relevant semantic guards.
- [ ] Prepare shape traversal without changing order, errors or rollback.
- [ ] Validate source and installed consumers, then matched benchmarks.
- [ ] Record evidence and submit a concrete review result.

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

Implementation pending. Baseline beartype 0.23.1 still requires supported
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
