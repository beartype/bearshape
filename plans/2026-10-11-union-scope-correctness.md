# Preserve state across internal alias checks


This living ExecPlan follows `PLANS.md`. Keep Progress, Surprises & Discoveries,
Decision Log and Outcomes & Retrospective current.

## Purpose / Big Picture


A late type alias is part of the enclosing check. It must see earlier dimension
bindings and function arguments, and successful bindings must constrain later
arguments. A separate decorated call or public DOOR call must remain independent.
The previous local upstream proposal passes 22 union regressions but fails eleven
new cases involving alias ownership and a caught nested failure. Develop a
supported scope interface and preserve all native composition and errors.

## Progress


- [x] (2026-10-11) Inspect the previous proposal and the additional failing cases.
- [ ] Commit this plan and open a draft PR before implementation.
- [ ] Add a public lazy scope API to the local upstream proposal and adapt bearshape.
- [ ] Add alias ownership and nested-failure regressions; demonstrate old failures.
- [ ] Preserve an independently applicable upstream patch series and reproducible CI.
- [ ] Validate exact installed wheels, upstream units, runtime consumers and checkers.
- [ ] Update evidence and prepare review. No main merge or publishing.

## Surprises & Discoveries


Composite forward references delegate to a generated DOOR checker. Treating that
internal frame as a public DOOR invocation silently separates shape state. A
boolean local marker demonstrated the distinction but is not a public integration
API. A second defect allows a rejected late leaf to leak mutations when an outer
predicate catches the violation and succeeds.

## Decision Log


Decision: Stack on PR #45, the combined release candidate, and keep optimization
in a subsequent focused PR. Rationale: correctness must be reviewable independently
of fast paths, with the same baseline fixes and memo performance on both sides.
Author/date: Codex, 2026-10-11.

Decision: Prepare upstream changes locally and carry source patches as review
artifacts in bearshape. Do not open an upstream PR or contact a maintainer.
Rationale: the user explicitly requested development before contact. These patches
are never imported, installed automatically by bearshape, or published.
Author/date: Codex, 2026-10-11.

Decision: Expose `beartype.plug.get_hint_check_scope()` and `HintCheckScope`. The
scope provides invocation-owned state, owner code identity and lazily bound
arguments. Internal aliases share the enclosing scope; independent generated
entry points create separate scopes. Ordinary checks allocate no scope unless a
plugin asks for it. Keep the released-dependency fallback in bearshape.
Author/date: Codex, 2026-10-11.

## Outcomes & Retrospective


Implementation is pending. Published beartype 0.23.1 still lacks the protocol.
Passing proposal tests does not authorize changing release readiness or claiming
support in the published dependency.

## Context and Orientation


`src/bearshape/_memo.py` currently finds generated beartype frames and stores a
ShapeMemo in frame locals. ShapeMemo holds scalar dimensions, variadic dimensions
and tree structures. Its snapshot and restore methods implement rollback.
`tools/upstream/test_union_transactions.py` contains 22 integration cases.
The local beartype proposal based on released v0.23.1, commit
f85b67d8b0b6bd9c910bd97f0d2d417c4550b038, adds the `__beartype_state__` hook and
transaction boundaries around composite checks. A transaction saves the current
state and restores it after failure. Existing proposal commit is
d0fe6e67a5ab693acb263e4bb0e1eb7131dc3fba. It is not a released dependency.

## Plan of Work


First preserve the original proposal as `tools/upstream/patches/0001-state.patch`.
Develop the correctness delta in a separate local upstream branch. Add a private
scope implementation exported by `beartype.plug`, tag generated public entry
points and internal alias delegates explicitly, and retain separate checker
caches so public and delegated checkers never share scope semantics. A scope
contains no frame reference and is created only when requested; frame ownership
ends with the check. Argument binding remains lazy and uses the original callable.

Adapt `_memo.py` through the public API when available, retaining released-0.23.1
behavior otherwise. Always give a stateful late leaf its own checkpoint so a
caught rejection cannot contaminate the caller. Preserve new regressions in
`tools/upstream/test_scope_transactions.py`, with generic protocol tests in the
upstream patch. Add developer instructions and a proposal CI lane that builds
from the pinned upstream base plus reviewed patches. It must exercise normally
installed wheels and must never upload anything. Keep existing release gates.

## Concrete Steps


Work in this feature worktree using uv 0.11.17. Start with:

    uv sync --locked
    uv run --locked prek install
    uv run --locked pytest tests/ --ignore=tests/test_typecheck.py -n auto
    uv run --locked pytest tests/test_typecheck.py -q

For proposal validation, export locked tools excluding beartype, build a clean
upstream checkout with the ordered patches, build bearshape, and install both
wheels into fresh Python 3.11 and 3.14 environments. Run the environments directly;
`uv run --locked` would replace the proposal with published beartype. Copy tests
outside source checkouts to prove installed imports. Exact commands will be
recorded in `tools/upstream/README.md`. Stage files, run normal hooks and manual
actionlint, then commit implementation and evidence separately from the plan.

## Validation and Acceptance


The old proposal must fail the eleven demonstrated regressions. The new proposal
must pass all existing 44 combined integration/protocol cases and the sixteen
additional cases without skips. Add direct scope lifetime, argument binding,
independent invocation and public/delegated cache-order tests. Existing runtime
consumers and four checker engines must pass on both supported endpoints. Check
upstream unit tests and typing. State explicitly which optional backend or
platform cases are unavailable; no skips establish unsupported hardware evidence.

## Idempotence and Recovery


Keep the original proposal and published baseline environments unchanged. Use
separate local upstream branches and fresh artifact directories. Patches must
apply to the exact base with `git apply --check` and a clean checkout. No package
is monkeypatched, no user annotation is rewritten, and no upstream branch is
pushed. Main stays unchanged. Preserve evidence under the main checkout's ignored
`build/union-scope-development/` directory before any worktree cleanup.

## Artifacts and Notes


Record source commits, patch and wheel SHA256 hashes, interpreter versions, exact
commands, imported package paths, test counts and hosted run URLs. The reviewable
patch series is a development artifact, not a forked dependency for publication.

## Interfaces and Dependencies


Keep Python >=3.11 and released beartype 0.23.1 as the locked baseline. The proposed
public scope object exposes `state: dict[object, object]`, `owner_code: CodeType`
and `arguments: dict[str, object]`. Scope lookup returns None outside a generated
checking invocation. `__beartype_state__` remains a callable returning an object
with `snapshot()` and `restore(token)`; the snapshot token is opaque to beartype.
Optimization-specific promises are deferred to the next PR.

Revision note — 2026-10-11: Created the correctness and scope plan before code.
