# Close the combined candidate audit in focused changes

> Historical execution record. Versions, commands and pending actions below
> describe this work at the time. Use the [plan index](README.md),
> [current contributor guide](../CONTRIBUTING.md) and
> [current handoff](../docs/maintainers/production-readiness.md) for today's
> workflow, merge status and release prerequisites.


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
upstream proposal. The subsequent owner instruction on 11 October 2026
authorizes merging the validated stack, verifying main and cleaning merged
branches/worktrees while preserving every reviewed commit. Publication,
deployment and maintainer contact remain unauthorized.

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
- [x] (2026-10-11) M5: PR #52 normalizes strict, trusted Like and converted
  shapes and contains ordinary metadata exceptions. Twenty new cases include
  four malformed shapes, nine failing properties, converter-owned inspection,
  integer-index axes and cancellation. Failing-first evidence retained; NumPy,
  JAX, Torch and edge suites pass. Minimal consumer checks negative metadata.
- [x] (2026-10-11) M6: PR #53 uses weak keys in the root Like trust cache.
  Both lifetime regressions failed first; all 64 temporary protocol/native
  classes now collect, while stable native positive/negative checks still pass.
  The NumPy suite passes with only platform precision skips.
- [x] (2026-10-11) M7: PR #54 keeps Value binding lazy and directly reuses
  owned array leaf validators, retaining all snapshots. Four optimization
  guards failed first; expanded nested rejection, fresh metadata and seven
  composition guards pass. Full runtime/four-checker push hooks pass. Matched
  installed measurements on 3.11/3.14 with both released/proposed beartype show
  strict checks about 44–62% faster and Tree/100 about 50–61% faster. Raw samples,
  construction costs, limitations and hashes are in
  `tools/evidence/2026-10-11-audit-performance/`.
- [x] (2026-10-11) M8: PR #55 collects all four composition modules,
  adds the separate compatible-dependency nightly canary and tests its strict
  preflight boundary. Native custom/Structured alias consumers pass all four
  checkers, including explicit consumer-root resolution for Pyrefly. Current
  changelog/handoff and developer release guidance are refreshed. Normal hooks,
  actionlint, rendered docs/95 snippets and all 29 notebook cells pass.
- [x] (2026-10-11) M9: `codex/audit-integration-review` preserves all 21
  open PR heads. Both Python endpoints pass 1,300 normally installed baseline
  tests and 1,427 proposal tests, plus the original 23 audit regressions with
  each dependency. Fresh minimal environments, 91.10% branch coverage, normal
  hooks, actionlint, rendered docs and both notebook endpoints pass. All eight
  focused PR heads have 36 successful hosted checks; both new hosted dependency
  canaries pass. Exact identities and remaining release prerequisites follow.
- [x] (2026-10-11) Owner approved merging the validated stack with all reviewed
  commits preserved, followed by main verification and merged-worktree cleanup.
  The closeout record is retained outside worktrees in `build/merge-closeout/`.
- [ ] External: supported upstream release, approved repository/PyPI controls,
  exact final CUDA evidence and separately authorized publication.

## Surprises & Discoveries


The audit's 23 new cases fail on both installed Python endpoints while existing
suites pass. Arithmetic, mixed variadics and Tree ownership also fail with the
published dependency, independently of the proposed upstream protocol. Current
release CI runs the original 22 union cases but omits 40 later scope cases.

Hosted NumPy-only lanes exposed a misplaced Tree optimization guard, which
required optree. Move that guard into the Tree module and retain independent
strict/Like guards in the NumPy-compatible memo suite; no test is removed.

Installed proposal consumers inside a checkout exposed Pyrefly loading different
ancestor configurations for dependency files. Pin its configuration to the copied
consumer pyproject, alongside the consumer search root and selected interpreter.
The failing positive dtype-identity consumer remains unchanged.

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

Decision: merge approved stacked heads into their actual bases without rewriting
commits, then merge the complete integration PR into main. Verify every saved
review head is reachable, main's CI and archive identity, and preserve ignored
evidence before removing only clean merged worktrees and branches. Replace live
links to disposable branches with durable destinations. Rationale: explicit
owner approval now covers merge and cleanup, but not publication or contact.
Date/author: 2026-10-11, Codex.

## Outcomes & Retrospective


The six correctness fixes, measured optimizations and CI/docs work are implemented
in PRs #48–#55. No additional public feature was necessary. Nothing has been
merged at the pre-merge review recorded below. Merge and cleanup are now
authorized and their final evidence belongs in `build/merge-closeout/`. Nothing
has been published or deployed; the upstream proposal has not been sent. Local
and hosted CPU evidence is complete for the tested implementation below. Release
readiness remains withheld for the supported upstream dependency, fresh CUDA
evidence and owner-controlled prerequisites.

### Final implementation validation

Tested implementation: `dc3c58a936959440bbfb12fc8e45a536ba49e67f` (PR #55).
The separate integration branch includes every original PR head (#32, #34, #35,
#38–#47) and every audit-fix head (#48–#55). Main remains
`c0874f34615ca3797b24601a91324f3c9beb462a`. Later plan/handoff-only commits do not
change the package or copied consumer tests; verify identical archives when
building them.

- Source-derived bearshape wheel SHA256:
  `1e0bf25f4ad018d661d28b84a9136ade8f4f809a5c54c745a213c22d52284897`.
- Source archive SHA256:
  `cb30f2b46cdec4e602fdeeff7372c1be9185cb43bdfe43cc33ed63f47d931527`.
- Published beartype 0.23.1 wheel SHA256:
  `4461b4dc57e3fdd6c8a8464b22cf118002eea107c33e9fef651c69068ab3cce3`.
- Unchanged proposal beartype wheel SHA256:
  `0580ede1fe87229728b42674d45fb8c32ce09a7e348f962cc2741304ef2f10d8`.

`check_installed.py` passes 1,300 cases on CPython 3.11.15 and 3.14.5 with
published beartype. `check_upstream_proposal.py` applies the hash-checked series
to clean pinned source, builds normal installs, verifies origins, and passes
1,427 cases on both endpoints: those baseline cases plus 69 bearshape composition
cases and 58 upstream protocol/mixin cases. Both routes include all four static
engines' positive, negative and inference consumers. The five skips are the
missing CuPy module and four platform extended-precision cases; none is union
or scope validation.

All 23 original audit regressions pass on each endpoint with both published and
proposed beartype. Fresh minimal venvs contain only the candidate and declared
runtime dependencies, pass custom/variadic checks, and import no optional backend.
Source runtime coverage is 91.10%, above the unchanged 90% floor. Normal hooks,
actionlint, all 95 documentation snippets, changed rendered structures and all
29 notebook cells on each endpoint pass. The final wheel is byte-identical to
the measured optimized wheel, so the committed performance evidence applies.

The complete published-dependency release suite still fails honestly: 58 failures
and 11 passes out of 69 cases on each endpoint, plus the original failing probe.
No case is hidden, skipped or marked xfail. The proposal passes all of them.
The validation-only release run uses `publish=false`:
[expanded release gate](https://github.com/beartype/bearshape/actions/runs/38170318585).
Its conclusion and exact job evidence are retained in the local review packet;
a deliberately blocked run is not release readiness.

[PR CI](https://github.com/beartype/bearshape/actions/runs/38170264797) and
[proposal CI](https://github.com/beartype/bearshape/actions/runs/38170264778)
provide 36 successful checks on the implementation head. The two new
[dependency canaries](https://github.com/beartype/bearshape/actions/runs/38170316908)
pass and retain resolved locks, versions and test output. Local full logs,
archive identities, original regressions and administrative snapshots are in the
ignored `build/audit-followup/` review packet.

## Context and Orientation


`src/bearshape/_dimensions.py` formats runtime and symbolic expressions;
`src/bearshape/_shape.py` binds and compares dimensions. `src/bearshape/_memo.py`
resolves per-invocation state; at the audited baseline, `_tree.py` pushed an
unconditional memo while checking leaves. That shared intended leaf state but
also captured independent public checks. `_array_types.py` validates strict/Like
metadata and held a strong class-keyed trust cache at that baseline. Backend
modules expose runtime factories and checker-only native aliases. `tools/upstream/` contains unshipped integration
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

Revision 2026-10-11: record explicit merge/verification/cleanup approval and
keep branch-deletion-safe evidence links; publication and contact remain separate.
