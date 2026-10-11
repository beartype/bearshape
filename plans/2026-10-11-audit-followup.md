# Close the combined candidate audit in focused changes


This living ExecPlan follows `PLANS.md`. Keep Progress, Surprises & Discoveries,
Decision Log, and Outcomes & Retrospective current. It extends the reviewed
release and union plans already in this branch.

## Purpose / Big Picture


Users must receive correct shape contracts even when they combine arithmetic,
broadcast dimensions, Tree predicates, ragged trees and custom array protocols.
The combined candidate audit at 89d84268cf500f576bd0f784df8912c6f5af5d5c found
six local gaps despite 1,262 passing installed tests per Python endpoint. Close
those gaps with failing-first regressions, then reduce measured overhead and
complete release CI and developer documentation. Keep Python 3.11–3.14 and
released beartype 0.23.1 as the baseline while separately validating the local
upstream proposal. No publication, deployment, maintainer message or main merge
is authorized by this implementation request.

## Progress


- [x] (2026-10-11) Audited the combined head, including all thirteen open PR heads;
  retained 23 failing audit cases, a 676-case broadcast matrix and raw evidence.
- [x] (2026-10-11) Owner authorized all audit fixes in focused PRs, correctness
  before optimization and CI/docs; explicitly prohibited publishing/contact.
- [x] (2026-10-11) M1: PR #48 preserves grouping with 64 arithmetic table cases
  and three public decorator-mode regressions; failing-first evidence retained.
  Dimension/NumPy suites pass with only platform precision skips.
- [x] (2026-10-11) M2: PR #49 retains strict variadic targets. Five new tests
  failed first; the 676-pair matrix, equal-shape transition and public decorator/
  return checks now pass. The minimal consumer also checks strict transitions.
- [x] (2026-10-11) M3: PR #50 uses a public beartype leaf wrapper with
  explicit memo ownership. All 12 isolation cases failed first, then passed;
  cross-leaf/outer Value, parameter/return, exception rollback and lifetime tests
  pass. Tree/JAX baseline suites pass; 189 Tree/proposal source tests pass with
  the optimized upstream patch. Exact installed validation follows in M9.
- [x] (2026-10-11) M4: PR #51 checks suffixes on every terminal path.
  Twenty-two paired-backend cases cover valid/mismatching ragged shapes,
  multi-name suffixes, empty containers, shared bindings and rollback. Tree/JAX
  suites pass. Rendered docs and all 94 Python snippets validate; changed
  paragraphs were inspected in the generated HTML.
- [ ] M5 in progress: focused metadata PR follows #51. Normalize dimensions
  through the integer-index protocol, reject negative sizes, preserve readable
  failures and cancellation, and let selected converters inspect untrusted inputs.
- [ ] M6: Open lifetime PR, stop default Like trust caching from retaining transient classes.
- [ ] M7: Open performance PR after correctness; keep Value arguments lazy and measure.
- [ ] M8: Open CI/docs PR; complete composition gates, consumer typing recipes and handoff.
- [ ] M9: Validate the complete stack, exact archives and both dependency configurations;
  present PRs and remaining external prerequisites for review.
- [ ] External: supported upstream release, approved repository/PyPI controls, exact final
  CUDA evidence, merge approval and separately authorized publication.

## Surprises & Discoveries


The audit's 23 new cases fail on both installed Python endpoints while existing
suites pass. Arithmetic, mixed variadics and Tree ownership also fail with the
published dependency, independently of the proposed upstream protocol. Current
release CI runs the original 22 union cases but omits 40 later scope cases.

## Decision Log


Decision: use a stack of focused branches/worktrees starting at PR #47, with a
plan commit and draft PR before each implementation. Each PR states its actual
base and focused scope. Rationale: the candidate already contains reviewed,
unmerged work; preserve that ancestry and avoid merging into an active PR's base
before approval. Date/author: 2026-10-11, Codex.

Decision: preserve the documented leaf-adjacent meaning of Tree suffixes and
retain valid ragged trees. Strict variadics remain exact once established.
Rationale: the owner accepted the audit recommendations and requested preserved
functionality; silently weakening constraints or rejecting all ragged trees
would not meet that request. Date/author: 2026-10-11, Codex.

Decision: keep unsupported upstream adoption and owner-controlled publication
settings explicit. Rationale: patches do not constitute a published dependency,
and the missing environment reviewer and private publisher identity cannot be
invented. Date/author: 2026-10-11, Codex.

## Outcomes & Retrospective


Implementation is in progress. Nothing has been merged or published. Completion
of local changes will not itself establish release readiness.

## Context and Orientation


`src/bearshape/_dimensions.py` formats runtime and symbolic expressions;
`src/bearshape/_shape.py` binds and compares dimensions. `src/bearshape/_memo.py`
resolves per-invocation state; `_tree.py` currently pushes an unconditional memo
while checking leaves. This shares intended leaf state but also captures
independent public checks. `_array_types.py` validates strict/Like metadata and
holds a strong class-keyed trust cache. Backend modules expose runtime factories
and checker-only native aliases. `tools/upstream/` contains unshipped integration
patches and tests, distinct from ordinary baseline tests in `tests/`.

The candidate remains 0.1.0rc1. `docs/maintainers/production-readiness.md` contains
historical evidence that must remain dated. `docs/maintainers/releasing.md` owns
future publication instructions; `.github/workflows/validate.yml` shares normal
validation and `pypi.yml` adds the release contract and immutable artifact gate.

## Plan of Work


M1 groups each expression operand and unary operand without changing public
syntax or losing Value scope. Add arithmetic table cases and decorated positive/
negative consumers in `tests/test_dimensions.py` and `tests/test_numpy.py`.
Observe size=2 accepting `(size+1)*2 == 6`, rejecting 4, and `(-N)**2` accepting 4
when N=2. Update the changelog, then validate before committing the implementation.

M2 corrects `_check_variadic`: equal-shape matches retain stricter constraints;
broadcast-only bindings may accumulate a common target, but a strict occurrence
fixes that target. Add both-order pairs and strict/broadcast/strict transitions,
zero axes, rank differences, returns and the no-optional-backend smoke check.

M3 replaces Tree's unconditional context with ownership limited to intended leaf
checking. Prototype using a public beartype-decorated leaf checker whose code is
known, so explicit memo ownership can distinguish it from nested independent
checks. Preserve composite leaves and original outer Value arguments. Validate
both tree backends, decorator modes, DOOR, aliases, errors, rollback and lifetimes
against released and proposed upstream. Do not modify upstream internals.

M4 traverses suffix constraints relative to leaf-adjacent containers, not just
the globally deepest breadth-first layer. Validate matching and differing ragged
branches, several suffix names, empty containers and backend agreement. Clarify
mixed-depth examples in `docs/features/tree-annotations.md`.

M5 normalizes custom metadata with integer-index dimensions and nonnegative
sizes, preserves ordinary diagnostic failures, and avoids accessing untrusted
input properties before a selected converter. Catch ordinary metadata exceptions
without swallowing BaseException/cancellation. Preserve original arguments and
avoid optional backend imports for strict custom arrays.

M6 removes strong ownership of transient classes in the root Like fast-path
cache, with collection and native-path regressions. Do not conflate this cache
with annotation identity caches or introduce arbitrary value caching.

M7 profiles the corrected candidate first. Avoid binding arguments in annotations
without Value expressions, and reduce repeated Tree leaf setup only through a
safe owned path. Precompute invariant annotation work if measurements justify it.
Retain snapshots, all-leaf traversal, dtype freshness, exception semantics and
weak-reference evidence. Compare matched normal installs on the same interpreter
and keep raw benchmark samples; timing is not a CI pass threshold.

M8 runs all composition/scope tests as a release gate on the exact installed
wheel and normally available dependency. A separate proposal test remains useful
but cannot authorize publication. Add a separate dependency-upgrade canary if it
can keep the locked release lane deterministic. Add tested native TYPE_CHECKING
alias recipes for custom factories and Structured, refresh current evidence and
consolidate the Unreleased changelog without altering historical plans.

M9 builds an integration review branch preserving all focused heads, validates
combined source and normally installed archives, and records hashes, versions,
commands and results. Verify the published union blocker still fails honestly.
Prepare concrete administrative settings and exact-wheel GPU commands for later
owner action; do not claim older GPU results cover new state code.

## Concrete Steps


Use uv 0.11.17 (the existing local tool executable) from each worktree root:

    uv sync --locked
    uv run --locked prek install
    uv run --locked pytest tests/ --ignore=tests/test_typecheck.py -n auto
    uv run --locked pytest tests/test_typecheck.py -q
    uv run --locked prek run -a
    uv run --locked prek run actionlint -a --stage manual

Run new regressions before editing implementation; save failing logs outside the
worktree. Stage new files before normal hooks. Real pre-push hooks run runtime
and checker validation. Follow `CONTRIBUTING.md`/`tools/README.md` for docs,
notebook, exact archives and minimal consumers. For patched upstream, follow
`tools/check_upstream_proposal.py` with clean source at the series base and fresh
output directories; invoke the created interpreter directly, never uv run that
would replace the patched dependency. Record hosted checks for each exact head.

## Validation and Acceptance


All 23 original audit regressions must pass after their fixes, alongside expanded
positive/negative cases and the existing CPU/four-checker suite. Array shapes,
Value scope, scalar/Like behavior and Tree registration remain intact. Rejected
alternatives and exceptions restore state; independent checks do not capture
Tree state; temporary classes and arrays can be collected. Root imports remain
backend-free. Optimizations must pass the same correctness suite and have matched
measurement evidence. Release gates must include the newer scope tests and fail
closed on the still-unsupported published dependency.

## Idempotence and Recovery


Keep main and existing PR heads intact. Every branch is additive, prefixed codex,
and backed by a matching worktree. Do not overwrite earlier artifact evidence,
force-push main, bypass hooks, suppress diagnostics or turn failures into xfails.
Use a new output directory if an artifact build fails partway. Git tooling across
repositories clears hook-local variables through the existing git_environment
helper. Owner-controlled settings remain pending until explicitly configured and
verified; absence of a reviewer decision is not permission to bypass approval.

## Artifacts and Notes


Original evidence lives in the main checkout's ignored
`build/full-audit-2026-10-11/`. New logs, exact archives, hashes and measurements
live in `build/audit-followup/` outside disposable worktrees. Record summary
results in this plan so repository reviewers do not depend on local files.

## Interfaces and Dependencies


Keep the public annotation API, supported backends/checkers and beartype 0.23.1
baseline. Use existing runtime validators, ShapeMemo snapshots, public beartype
entry points and the optional public scope adapter. No monkeypatch, bytecode
inference, replacement type checker or new public feature is part of this plan.

Revision 2026-10-11: initial authorized follow-up plan, with separate correctness,
optimization and release-documentation milestones and explicit external limits.
