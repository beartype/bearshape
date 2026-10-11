# Reduce ordinary checking overhead without weakening rollback


This living ExecPlan follows `PLANS.md` and the correctness plan
`plans/2026-10-11-union-scope-correctness.md`. Keep all living sections current.

## Purpose / Big Picture


Ordinary beartype users should not pay for state transactions after lazy references
are known to be plain classes. Keep first-call correctness, lazy resolution,
checker ordering, sampling and cache invalidation. Keep the correctness changes
independently reviewable in PR #46, and benchmark against published 0.23.1 as well
as the unoptimized correct proposal.

## Progress


- [x] (2026-10-11) Identify remaining tuple, mapping and nested-list overhead.
- [x] (2026-10-11) Committed plan and opened draft PR #47 before implementation.
- [x] (2026-10-11) Added known-domain and explicit atomic-leaf fast paths.
- [x] (2026-10-11) Added plain-class specialization and weak cache invalidation listeners.
- [x] (2026-10-11) Added eleven optimizer regressions; upstream units pass 467/475 cases on the endpoints.
- [ ] Validate exact installed wheels and measure matched endpoint benchmarks.
- [ ] Record performance limits and prepare PR review without upstream contact.

## Surprises & Discoveries


The assessment reduced ordinary `list[LateClass]` overhead, but tuple, mapping and
nested-list cases still added approximately 0.3–0.4 microseconds per call. Resolving
unselected references eagerly would change existing behavior. A fast checker must
capture resolved plain classes so concurrent cache clearing cannot introduce a
stateful hint into an expression that has already chosen the stateless path.

## Decision Log


Decision: Stack this PR on #46; keep the public scope API and rollback fixes in the
parent. Rationale: reviewers can assess semantics before optimization.
Author/date: Codex, 2026-10-11.

Decision: Never resolve references to enable a fast path. After native checking
has resolved every relevant reference to an ordinary class with the builtin
metaclass and no state hook, compile the same expression with those resolved
classes. Clear specialization alongside the upstream reference cache. Unknown,
custom-metaclass and composite-alias cases retain transactions. Rationale: avoids
stale capabilities, changed lazy errors, predicate replay and changed sampling.
Author/date: Codex, 2026-10-11.

Decision: Opt-in atomic leaves promise to restore all mutations on False or any
BaseException. Only such primitive roots may omit an outer duplicate snapshot;
composite parents still own rollback. Existing bearshape leaf checks satisfy this
promise. Rationale: remove redundant work without assuming arbitrary plugins are
atomic. Author/date: Codex, 2026-10-11.

## Outcomes & Retrospective


Implementation and measurements are pending. This is local upstream proposal work,
not a dependency release or publication authorization.

## Context and Orientation


The parent PR stores the pinned upstream base and ordered patches in
`tools/upstream/patches/series.json`. Its validator builds both wheels and checks
normally installed consumers. The upstream `_HintCheckState` saves plugin state
before a composite or alternative and rolls it back on failure. Unknown references
require a context so newly discovered state can join existing checkpoints. Fully
known domains need not publish a new context. A primitive atomic hint can handle
its own failed-leaf restoration while its parent still restores rejected branches.

## Plan of Work


Create a third upstream patch from the correctness head. Add an explicit atomic
leaf promise and the known-domain transaction variant. In the native expression
factory, keep a copy of the unwrapped expression and its lexical scope. For
expressions with references and no known state domains, create a dispatcher that
initially uses the transaction path. It may compile a direct plain-class expression
only after checking has resolved all proxies. Use the upstream cache lock to take
a consistent resolved snapshot. Register only weak invalidation listeners; cache
clear must release captured old classes immediately. In-flight checks may finish
against their captured pre-clear classes, but subsequent checks must re-resolve.

Add upstream regressions for cold stateful checks, unresolved alternatives, cache
clear from plain to stateful and back, custom metaclasses, sampling count, caught
exceptions, concurrent clearing and release of old classes. Extend the benchmark
with tuple, mapping and nested-list references, cold and warm samples, correctness
checks and raw repeats. Keep benchmark thresholds out of CI.

## Concrete Steps


Use uv 0.11.17. Follow the parent plan's locked baseline and hook commands. Export
`0003-ordinary-performance.patch` and update the series digest. Run
`tools/check_upstream_proposal.py` against fresh pinned upstream checkouts and new
output directories on Python 3.11 and 3.14, following `tools/upstream/README.md`.
Run upstream unit tests and pyright on the patched source. Compare the same
benchmark scripts in released, correctness-only and optimized environments, one
at a time while other tests are stopped. Use 20,000 calls and seven repeats;
record machine/interpreter versions and wheel/script hashes. Never compare an
incorrect union result as a valid faster implementation.

## Validation and Acceptance


All 67 parent focused cases must remain passing with no skips, plus the new
optimizer regressions. Full runtime consumers and four static consumer engines
must pass on both endpoints; ordinary locked baseline tests remain passing.
Ordinary reference overhead should materially decrease relative to correctness-
only without a native stateless regression beyond local measurement variability.
Record actual results even if a path cannot safely be optimized. No new release
claims, dependency lock changes, retry checks, global monkeypatches or xfails.

## Idempotence and Recovery


Use a separate local upstream branch and preserve parent wheels. The ordered
patch driver rejects mismatched inputs. Retry failed builds in fresh directories;
never erase earlier evidence. Store final logs and hashes under the main checkout's
ignored `build/union-scope-development/`. Main and upstream remotes stay unchanged.

## Artifacts and Notes


Record commit and patch identities, normally installed import origins, exact
commands, test counts, raw timing samples and hosted checks. Keep correctness and
optimization evidence separate. Publication remains blocked on supported adoption.

## Interfaces and Dependencies


Preserve `HintCheckScope` and the state getter protocol from #46. Add only the
optional `__beartype_state_atomic__ = True` promise on participating hint classes.
The optimization is internal and does not change beartype's public configuration,
annotation syntax, ordering, container sampling or DOOR semantics.

Revision note — 2026-10-11: Created the focused optimization plan before code.


Decision update — 2026-10-11: Keep root references and one sampled-reference list
on the existing proxy path. Extending specialization there changed the existing
root expression-factory identity contract; that broader change is unnecessary
for the requested composite overhead reduction. The small remaining state-hook
lookup cost is explicit. No existing upstream test was weakened or removed.
