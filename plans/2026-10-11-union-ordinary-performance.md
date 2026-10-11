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
- [x] (2026-10-11) Both installed endpoint suites pass 1,221 cases; matched sequential benchmarks are preserved.
- [x] (2026-10-11) Recorded exact artifacts, raw repeats and limits; implementation head has 36 passing hosted checks.

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


Implementation and measurements are complete in PR #47. This is local upstream proposal work,
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


## Completed evidence


Implementation head: 291af356856ce93ae87020cee8c4f18903e89d92. Local upstream head:
01f32470, based on correctness head 5071616b. Patch digests are recorded in the
series manifest. `tools/upstream/evidence/2026-10-11/README.md` contains matched
results and six raw benchmark files, using the same bearshape wheel in every
variant and sequential runs. All 17 runtime source files match that exact wheel.

The optimized bearshape wheel SHA256 is
fe593320362bee43e8f1f91bb3ec10d1b3f85a0ea1039a3b7f7b409302ad8026;
its tested source archive is
45465be260ff82d4baba1967613c1dcb4bdd90930706e820b693d0b62ba67e2b.
The local upstream wheel SHA256 is
777f5641545dc78c4eec30447c6ddfadec6144767e6466781210831ff50c85fa.
Copies, commands and endpoint logs survive under the main checkout's ignored
`build/union-scope-development/optimized/`. Subsequent documentation/evidence
commits change source archive contents but not these runtime wheel inputs.

Both Python 3.11.15 and 3.14.5 installed consumers pass 1,221 tests, with five
explicit skips (absent CuPy and four extended-precision platform cases). CPU
backend preflight and the unchanged union probe pass. Four checker consumers
retain positive, negative and inference assertions. Upstream unit tests pass
467/475 cases (15/7 interpreter or optional-dependency skips). Upstream pyright
analyzes 483 files with zero errors or warnings. Normal hooks and actual push
runtime/four-checker hooks pass. PR #47 implementation head has 36 passing hosted
checks, including both proposal lanes in run 38142309440.

On 3.11 warm tuple/mapping/nested-list calls change from 1.107/1.126/1.147
microseconds in the correctness proposal to 0.162/0.193/0.213. Released 0.23.1 is
0.672/0.693/0.723 on those same inputs. On 3.14 optimized medians are
0.176/0.214/0.245. Strict shape checking falls from 9.816 to 7.600 on 3.11 and
10.313 to 7.905 on 3.14. Correct fallback unions take 12.205/12.482; the released
baseline is incorrect and is never presented as a valid timing comparison.
Root references and simple sampled lists retain approximately 0.06–0.07
microseconds extra cost on 3.11. Custom metaclasses and stateful aliases remain
general. Native checks stay around 0.09 microseconds. This is local evidence,
not a cross-platform performance guarantee or a release readiness claim.

Revision note — 2026-10-11: Completed and validated the focused optimization,
recorded raw matched measurements and exact artifacts, and retained explicit
remaining costs. No existing regression or diagnostic was suppressed.
