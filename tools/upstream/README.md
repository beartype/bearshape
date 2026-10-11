# Native union integration proposal

## Current correctness proposal

PR #46 supersedes the earlier ownership design. The previous proposal passed 22
union cases but failed eleven additional alias and caught-failure regressions.
The scope interface is now `beartype.plug.get_hint_check_scope()`: it returns an
invocation-owned `HintCheckScope` with a private-keyed `state` dictionary,
`owner_code`, and lazily bound `arguments`. Internal alias checks share the
caller; nested decorated and public DOOR checks remain independent. No frame or
context token is retained by a scope. Ordinary users allocate no scope unless a
plugin requests one. bearshape keeps its released-0.23.1 fallback.

`patches/series.json` pins the released upstream base and SHA256 of each ordered
patch. `0001-state.patch` preserves the original state protocol proposal;
`0002-scope-correctness.patch` adds the public scope API and independent
rollback for a rejected late leaf. These files are review artifacts, never
runtime code loaded or automatically applied by bearshape. The local wheels
still identify as 0.23.1; they are **not the published beartype 0.23.1 wheel**.

Create a disposable clean checkout of beartype at
`f85b67d8b0b6bd9c910bd97f0d2d417c4550b038`. From this bearshape checkout, run:

```sh
uv run --locked python tools/check_upstream_proposal.py \
  --upstream-source /path/to/clean/beartype \
  --output /path/to/new/proposal-evidence --python 3.11
```

Repeat with a second clean upstream checkout, a new output directory and Python
3.14. The driver rejects a dirty/wrong-base checkout and changed patch hashes,
clears hook-local Git variables, applies the reviewed series, builds both
wheels, and runs copied consumers outside source checkouts in a fresh
environment. It includes all runtime tests, four static consumer engines, the
original union probe, scope regressions and upstream protocol/scope unit cases.
It writes exact commands, source base and artifact hashes to the output
directory. A partial failure leaves evidence intact; retry with fresh disposable
paths. Use the created environment's interpreter directly for additional
experiments.

The `Validate local upstream proposal` workflow runs these endpoint consumers
with read-only repository permissions. It has no publishing job or credentials.
This evidence supplements the released-dependency CI; it does not change release
gates, the dependency lock or the requirement for supported upstream adoption.

## Historical proposal evidence

The `test_union_transactions.py` suite exercises the proposed beartype
`__beartype_state__` protocol. It runs explicitly because the required upstream
change has not shipped. These tests are real failures on published beartype
`0.23.1`; they have no skips or expected-failure markers. Passing the normal
0.23.1 CI suite does not prove this integration.

The bearshape adapter exposes the existing `get_memo` function as a shared state
getter on its runtime-hint metaclass. It returns the active `ShapeMemo`, whose
`snapshot()` and `restore(token)` methods cover single dimensions, variadic
dimensions and tree structures. State is located once per checking expression.
Existing leaf validation remains necessary for rc0 and bare `isinstance` calls.

The original local proposal at upstream commit
`4aef992d1cd0a6d09fe5c3784523c44e0874b178` used a callback per snapshot. It
remains historical comparison evidence. The optimized proposal replaces that
interface with a state getter, compiles checking functions once, keeps simple
rollback records, and avoids unnecessary root snapshots and stateless-path
setup. Both proposals are based on upstream
`a2729e0e358bf963ee6f177e300ae08a622d05d6`, which identifies itself as
development `0.23.0rc1`. This version string does not imply acceptance or
publication. The optimized patch and exact commit are recorded in the focused
ExecPlan. Neither proposal is vendored or applied at import time.

## Reproduce

Apply the supplied patch to a clean checkout of the upstream base commit. From
this bearshape checkout, export the locked tools and backends while excluding
the upstream package being tested:

```sh
uv export --locked --no-hashes --no-emit-project --no-emit-package beartype \
  --output-file /tmp/bearshape-union-requirements.txt
uv venv /tmp/bearshape-union-env --python 3.11
UV_TORCH_BACKEND=cpu uv pip install \
  --python /tmp/bearshape-union-env/bin/python \
  -r /tmp/bearshape-union-requirements.txt \
  /path/to/patched/beartype .
/tmp/bearshape-union-env/bin/python tools/probe_union.py
/tmp/bearshape-union-env/bin/python -m pytest \
  tests/ tools/upstream/test_union_transactions.py -n auto
```

Repeat in a separate Python 3.14 environment. The probe must pass, the new
regressions must pass without skips, and the existing runtime and four-checker
suite must remain green. Use the environment's interpreter directly: a later
`uv run --locked` would restore the published dependency from the lock.

To observe the published dependency's unresolved failure directly:

```sh
uv run --locked python tools/probe_union.py
uv run --locked pytest tools/upstream/test_union_transactions.py -n 0
```

Both commands currently fail. This is baseline evidence, not successful
validation. Once an upstream-supported release exists, update the dependency
floor, lock, exact-version preflight and shared CI together, and move these
regressions into the required `tests/` suite. Do not retain a separate optional
integration lane after adopting the dependency that fixes the defect.

## Verified behavior

The 22 integration cases cover selected and rejected alternatives, earlier
bindings, nested unions, parameters and returns, explicit scopes, Like and
variadic annotations, tree structure bindings, async calls, cancellation, thread
isolation, object release, `Annotated` predicates, container sampling, and
aliases resolved after decoration. Negative cases still reject wrong values and
dimensions with useful beartype violations.

The proposal preserves the upstream ordering and sampling rules. A later
argument failure does not cause a search for a different earlier alternative.
Hidden state changes inside arbitrary predicates are not discovered; the
stateful runtime hint must expose the state hook. Completed transactions release
their state references and are ignored by subsequent checks using a copied
execution context; the upstream proposal includes regressions for both cases.

Local CPU runs do not establish CUDA coverage for the changed artifacts. The
handoff report and ExecPlan record interpreter versions, checks and availability
separately from earlier GPU evidence.

## Measure overhead

Run the same benchmark script in each normally installed environment:

```sh
/path/to/environment/bin/python tools/upstream/benchmark_transactions.py \
  --calls 20000 --repeats 7
/path/to/environment/bin/python tools/benchmark_runtime.py \
  --calls 10000 --repeats 5
```

The transaction benchmark verifies each case before timing it. An incorrect
baseline is recorded as `correct: false`; its failure is not presented as a
faster valid implementation. The synthetic plugin fixture supports both local
proposal interfaces solely to compare their bookkeeping using identical inputs.
The actual bearshape adapter exposes only the current proposed interface.

Compare original bearshape with rc0 and the first proposal, then optimized
bearshape with rc0 and the optimized proposal. PR #35 independently reduces
frame-discovery work; include it in both sides of the latter comparison to avoid
attributing that improvement to upstream. Record versions, source commits and
artifact hashes, and keep raw repeat samples. Timing has no CI threshold.

The owner requested further optimization before any upstream contact and has a
direct Zulip contact. Discussion material is prepared locally for the owner; no
message has been sent.

## October 2026 refresh

The proposal now applies to upstream release tag `v0.23.1`, source `f85b67d8`.
Published 0.23.1 still fails 20 of the 22 integration cases. The locally built
port passes all 22 on Python 3.11.15 and 3.14.5, with the original union probe
unchanged. Normally installed module origins were checked. Upstream unit tests
passed 446 cases on 3.11 and 457 on 3.14, with 18/7
interpreter/optional-dependency skips; upstream pyright reports no errors. These
are proposal results, not claims about the published wheel.

The durable patch and logs are under the main checkout's ignored
`build/release-2026-10-11/`. The focused program plan records the current
Python/dependency baseline. No upstream push, PR or maintainer message has been
sent. Supported upstream adoption is still required before releasing bearshape
with the full composition contract.
