# Normalize builtin dtypes without retaining checked objects

## Purpose / Big Picture

Continue the approved audit optimizations from main `28e885837e61705d3d3295463874c3e0acf35ca8`.
Lazy Value arguments and owned Tree leaf validation are already merged. The
remaining profile shows NumPy dtype.name calculation consuming significant time
for every array and every Tree leaf. Normalize known builtin dtype classes once,
while reading each checked object's current dtype on every invocation. Keep
custom/extension dtype protocols, metadata errors, structured comparisons and
byte order unchanged. A separate PR will prepare invariant shape traversal.

## Progress

- [x] Compare the remaining validation worktree with main and preserve evidence.
- [x] Confirm both parents and both conflict resolutions already exist in main;
  remove the obsolete clean worktree and branch after verifying the history bundle.
- [x] Record current main profile and this plan before implementation.
- [ ] Open the focused PR, add regression guards, then implement normalization.
- [ ] Run source/installed/checker/minimal/proposal validation on Python endpoints.
- [ ] Record matched installed benchmarks and final evidence; request review.

## Surprises & Discoveries

The old validation head c53d14f contains only a merge of two existing parents.
Its conflict resolutions join existing tests and changelog bullets; no unique
runtime behavior remains. Its complete history is in the verified
`build/merge-closeout/post-merge-history.bundle`. Generated docs, environment
versions and the comparison are in `build/remaining-optimization/cleanup/`.

The existing profile records 200,000 dtype.name calculations for 1,000 checks
of a 100-leaf input and return. Timing claims require new matched installations;
profile attribution alone is not a speedup measurement.

## Decision Log

- 2026-10-11: Optimize identities of known immutable builtin NumPy dtype classes,
  never arbitrary dtype instances, class names, checked values or their results.
  Root imports stay backend-free; custom properties remain live. This is a
  measured hotspot, not authorization for general caching or new syntax.
- Keep the published beartype 0.23.1 baseline and the separate upstream proposal.
  Reassess the remaining ordinary forward-reference cost without broadening the
  code-factory contract or changing reference invalidation/exception timing.

## Outcomes & Retrospective

Implementation pending. Release readiness remains withheld; no publication,
upstream communication or repository administration is part of this work.

## Context and Orientation

`src/bearshape/_dtypes.py` extracts canonical names and matches DtypeSpec.
Strict arrays and Like checks share it; Tree's owned leaf path delegates to
those same checks. `tests/test_dtypes.py` covers builtin and extension dtype
behavior. `tools/benchmark_runtime.py` measures native controls, strict/Like,
Value and complete Tree traversal. Historical scope improvements are recorded
in `tools/evidence/2026-10-11-audit-performance/`; compare this change to main,
not to the older pre-optimization baseline.

## Plan of Work

Add guards for mutable custom dtype properties, spoofed class names, fresh array
dtype changes, extension dtype fallback and release of user objects held by dtype
metadata. Only builtin class identities may have prepared canonical names; no
checked object or dtype instance may enter persistent state. Extend benchmarks
with representative normalization/casting controls, use the same script on both
sides, and record raw timings plus wheel hashes. Evaluate a direct loop for Like
casting only if it removes measured repeated setup without changing targets or
exception handling. Do not add an unsupported target cache.

## Concrete Steps

From this worktree use locked uv 0.11.17: `uv sync --locked`, then
`uv run --locked prek install`. Add and exercise focused tests before changing
runtime code where practical. Run the standard runtime and four-checker routes,
normal hooks, normal installed-wheel consumers and fresh minimal consumers.
Use `tools/check_upstream_proposal.py` on clean pinned beartype sources for the
full composition contract at Python 3.11 and 3.14. Preserve commands and hashes.

## Validation and Acceptance

Every current passing behavior remains passing, including mutable metadata,
custom dtype access, all Tree leaves/snapshots, rollback and object collection.
Known builtin normalization avoids repeated name calculation, while fake or
extension dtype classes remain on their original protocol path. Installed
benchmarks must demonstrate improvement without hiding ordinary controls,
construction costs, conversion scaling or unfavorable cases. No CI timing gate.

## Idempotence and Recovery

Keep main unchanged and work on codex/dtype-normalization. The obsolete worktree
can be recovered from its verified Git bundle. Fresh benchmark environments and
outputs may be regenerated from pinned artifacts. Revert an optimization if
semantic preservation or its performance value cannot be demonstrated.

## Artifacts and Notes

Local cleanup evidence: `build/remaining-optimization/cleanup/assessment.json`.
Current runtime source is main 28e8858; prior released/proposal test results are
historical until validation of this changed wheel completes.

## Interfaces and Dependencies

No public API, annotation spelling, Python range or dependency change.
Use existing DtypeSpec, array checker and backend boundaries. Do not retain
user-defined classes/objects in a new cache. Keep 2-space Python indentation.

Revision note — 2026-10-11: Created before implementation for the approved
remaining optimization work.
