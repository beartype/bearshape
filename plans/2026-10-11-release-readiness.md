# Prepare bearshape for Python 3.11 and released beartype


This living ExecPlan follows `PLANS.md`. Keep Progress, Surprises & Discoveries, Decision Log, and Outcomes & Retrospective current. It supersedes the current-version decisions in the September production roadmap while preserving that plan's historical evidence.

## Purpose / Big Picture


Scientific Python users should be able to install the next bearshape candidate on Python 3.11–3.14 with released beartype, use every existing annotation and backend, and receive correct shape, dtype and tree errors. A rejected native union alternative must never leave dimension bindings behind. Developers should have one documented route from a reviewed source commit to tested archives and, only after a separate release decision, publication of those exact archives.

The owner requested addressing the entire October audit in focused PRs, selected Python 3.11+ and beartype 0.23.1 as the baseline, and explicitly prohibited publishing now. Implement and validate the work; do not publish to PyPI, create a release, deploy Pages, or change account/repository access controls as part of implementation. Merge remains subject to review of concrete results. A local upstream prototype is not a published supported dependency.

## Progress


- [x] (2026-10-11) Audited main c0874f34615ca3797b24601a91324f3c9beb462a and all three open PRs. Preserved raw results and independent reproducers under the main checkout's ignored `build/audit-2026-10-11/`.
- [x] (2026-10-11) Recorded the owner's Python 3.11+, beartype 0.23.1 and no-publication decisions; created the program worktree before implementation.
- [ ] Commit this plan and open its draft PR before changing implementation.
- [ ] M1: Adopt the coordinated Python/dependency baseline and path-safe tooling in a focused PR.
- [ ] M2: Fix nested Value expressions, malformed converters, backend-free broadcasting and Tree grammar with failing regressions in focused PRs.
- [ ] M3: Refresh the existing upstream union proposal against 0.23.1, validate both projects, and prepare the supported integration route; resolve PR #34 conflicts without losing historical evidence.
- [ ] M4: Validate and reconcile existing action-update PR #32 and memo-performance PR #35, preserving their reviewed heads.
- [ ] M5: Implement candidate validation and publication controls, exact-artifact evidence and a developer release runbook in a focused PR.
- [ ] M6: Validate the combined source, four checker consumers, minimum dependency lanes, archives, documentation, notebook and actual CUDA hardware where available.
- [ ] M7: Present the review packet with PR disposition, evidence, external prerequisites and merge readiness; do not publish.
- [ ] Merge approved heads, verify reachability and main, then remove only clean merged worktrees. No merge approval has yet been requested for this program.

## Surprises & Discoveries


The audited ordinary suite passed 1,101 cases on Python 3.10 and 3.14 with released beartype 0.23.1, including four static checker engines. The 22 separate native-union cases still had 20 failures and two passes, even against PR #34's exact adapter. beartype 0.23.1 has the public diagnostic plugin but not the proposed state transaction protocol. Updating metadata cannot close that defect.

Four independent existing defects were reproduced: nested `Value` arithmetic loses function-value scope; custom converters returning None bypass validation; custom variadic broadcasting imports optional NumPy; and invalid interior/repeated Tree ellipses are silently discarded. All need behavioral regressions, not broad rewrites.

The host's global uv 0.12.22 is outside this repository's supported 0.11 range. An isolated locked environment already contains uv 0.11.17. Use that executable or install/bootstrap the documented version; do not loosen the constraint merely to accommodate this host. macOS aliases `/tmp` to `/private/tmp`, exposing two origin checks that canonicalize only one side of a path comparison.

## Decision Log


Decision: Require Python >=3.11 and beartype >=0.23.1,<0.24, with exact 0.23.1 in the lock and validation lanes. Rationale: explicit owner direction on 2026-10-11; Python 3.10 support and the rc0 baseline are superseded. Full composition remains blocked until supported upstream integration is available. Author: owner/Codex.

Decision: Keep supported interpreter claims at 3.11–3.14 initially. Rationale: Python 3.15 and free-threaded Python have no complete backend/checker/artifact proof; a >=3.11 metadata floor does not itself claim those combinations. Evaluate availability without silently adding new promises. Author/date: Codex, 2026-10-11.

Decision: Prepare 0.1.0rc1 as the next independent bearshape candidate. Rationale: the changed interpreter floor and behavior warrant a new candidate identity; publication remains separately prohibited. Author/date: Codex, 2026-10-11.

Decision: Preserve native composition and existing public syntax. No upstream monkeypatch, replacement checker, bytecode inference, xfail, weakened negative fixture, or restricted union support may make the gates green. Rationale: owner contract and actual correctness. Author/date: Codex, 2026-10-11.

Decision: Use separate reviewable branches for baseline, each independent runtime fix, and release automation; use a separate integration branch to combine them and existing PR heads. Rationale: surgical review and preservation of contributors' history. Update draft PRs before any implementation milestone. Author/date: Codex, 2026-10-11.

Decision: Do not send an upstream maintainer message or apply administrative controls without the appropriate authorization. Prepare the concrete tested upstream patch and exact settings first. Rationale: existing owner policy distinguishes code preparation from external contact and access changes. Author/date: Codex, 2026-10-11.

## Outcomes & Retrospective


Planning is recorded. Implementation, integration, merge and release readiness remain separate outstanding states. The hard external limitation is that the required transaction protocol has not shipped in 0.23.1. This must be reported explicitly even if all independent improvements are ready.

## Context and Orientation


`src/bearshape/_dimensions.py` represents dimensions and trusted developer `Value` expressions. `_shape.py` compares integer shape tuples and binds named/variadic dimensions. `_array_types.py` implements strict arrays and Like conversion; Like validates a converted value while preserving the caller's original argument. `_tree.py` implements runtime Tree specifications with optree's default registry. `_runtime_hints.py` supplies the metaclass used by generated hints. `_memo.py` owns invocation-local bindings and their snapshot/restore operations. `_decorator.py` controls explicit scopes; bare `@check` remains scope-only and `@check(conf=...)` invokes beartype.

A transaction means taking snapshots of participating validator state, checking a whole expression or alternative, retaining changes on success, and restoring changes on rejection or exception. A leaf check cannot observe that a later ordinary str check rejected its surrounding tuple. The upstream checker must expose that boundary. `tools/probe_union.py` reproduces the problem; PR #34 has 22 expanded cases in `tools/upstream/test_union_transactions.py` and a `__beartype_state__ = staticmethod(get_memo)` adapter.

Main is c0874f34615ca3797b24601a91324f3c9beb462a. Existing unmerged PR #32 updates checkout/setup-uv actions (head b0aac01849f952e95cb72c9220a546fb86fd64af). PR #35 filters irrelevant frames before reading locals (head f4084ebd1f74610317d27e0d2a8595f39335203d). PR #34 proposes union transactions (head 66bc3b93a746c2430aa4b4d983fa057f4608539a) and conflicts with newer ownership documentation. Preserve all heads and worktrees. The local upstream proposal is `/Users/ale/Code/beartype-union-transactions`, head 76e27706fb137c6a676ee7b79a66d8b3092b52ad based on a2729e0e358bf963ee6f177e300ae08a622d05d6. It is source work, not an accepted published API.

`pyproject.toml`, `uv.lock`, `tox.toml`, checker configuration, `tools/validate_runtime.py`, `tools/validate_tox_env.py`, `tools/check_installed.py`, and `.github/workflows/validate.yml` jointly define tested support. The shared workflow runs CPU backends, four checker engines, compatibility floors, documentation, notebook, archive and normal wheel consumers. Required validation aggregates every required lane. Actual CuPy runtime evidence requires a CUDA device.

`tools/check_release.py` checks version/tag/source identity, while `tools/check_distribution.py` checks wheel/sdist contents and hashes. `.github/workflows/pypi.yml` resolves a source, calls shared validation, records artifacts, and grants OIDC upload permission only to the environment-gated publishing job. OIDC is short-lived identity-based authentication; no stored upload token is needed. Existing private PyPI trust and GitHub protections remain unverified/incomplete and are not fixed merely by editing YAML.

## Plan of Work


### M1: A coherent released dependency baseline


Create `codex/python311-beartype0231` with a focused plan PR. Change requires-python, classifiers, `.python-version`, Ruff and four checker defaults, hook Python, tox names/validation, CPU/checker/compatibility/minimal/installed/notebook workflow matrices, exact dependency preflights and current documentation together. Remove obsolete 3.10 lanes and set beartype 0.23.1 everywhere current. Regenerate `uv.lock` using uv 0.11.17; verify backend floors actually resolve on 3.11. Preserve historical plan/evidence strings rather than blanket replacing the repository. Canonicalize both package origin and environment prefix in minimal/installed checks. Document the supported uv bootstrap.

Add focused compatibility regressions for the dataclass self-forward-reference fixed by 0.23.1 and deterministic container sampling via `BeartypeConf(is_random=False)`. Preserve direct caller-sensitive import-hook aliases. Document public `warn_if_beartype_claw_inactive()` only with an executed example/test; deterministic sampling means the first item, never every item. Run endpoint source/checker and preflight tests before proceeding.

### M2: Four independent correctness fixes


For Value arithmetic, recognize every `_ValueExpr` node rather than just its `Value` subclass in `_dimensions._binop`. Prove operand order, nesting, unary and attribute expressions, parameter and return checks, and wrong-value rejection. Preserve trusted expression evaluation rather than introducing a sandbox.

For custom Like conversion, make a converted None or malformed shape/dtype object an explicit validation failure rather than the success sentinel. Preserve converter exceptions as useful mismatch errors, no fallback conversion, original argument identity and memo rollback. Correct the public factory docstring. Cover DOOR boolean checks, decorated calls, diagnostics and later valid calls.

For variadic broadcasting, replace NumPy-only metadata calculation in `_shape._check_variadic` with tuple arithmetic respecting trailing alignment, dimension 1, zero-size dimensions and incompatible axes. Compare representative results with NumPy in full tests while extending the minimal normal-wheel smoke with valid and invalid custom arrays and zero optional imports.

For Tree grammar, reject more than one ellipsis and any interior ellipsis before removing the permitted single leading/trailing marker in `_tree._parse_spec_args`. Prove documented forms still work and malformed forms raise a useful TypeError immediately. Each fix gets its own failing regression, implementation, CHANGELOG entry and focused plan PR. Run relevant existing tests and normal hooks.

### M3: Correct union state through supported upstream integration


Fetch the released upstream v0.23.1 source into a separate checkout. Port the existing 13-file proposal without modifying installed upstream files or the recorded September worktree. Review upstream changes to code generation, lazy references, diagnostic traversal and context lifetime. Run the upstream protocol tests, complete relevant upstream unit tests and source checker. Normally install the new upstream source and bearshape adapter into separate environments; run the unchanged original reproducer, 22 integration cases and existing runtime/checker consumers on 3.11 and 3.14. Record exact commits, dependency origins and artifact hashes.

Resolve #34's ownership/documentation conflicts by merging current main while preserving its head. Keep a clear distinction between published 0.23.1 baseline failure and prototype success. Prepare a concrete upstream submission patch/body and performance evidence for owner review. Only after a normally available supported dependency exposes the protocol can the main dependency floor advance and transaction regressions move into mandatory source and archive tests. Until then, candidate release validation must fail visibly on the union contract; never count the ordinary suite as release acceptance.

### M4: Reconcile existing PRs and measure the combination


Inspect exact action revisions and runner requirements from upstream action metadata for #32; correct stale version comments when integrating. Revalidate #35's frame optimization with positive ownership, nested calls, async/thread and weak-reference cases on the new baseline. Measure matched normal installations before/after the filter and separately before/after transaction support; retain raw repeats, correctness flags and source hashes, with no flaky timing threshold in CI.

Combine reviewed branch heads in a dedicated integration worktree, resolving conflicts without dropping either side's changes or earlier source history. Keep #32/#35 independent until merge review. #34 remains a draft until its support boundary is concrete. Issue #37 stays open until an actual release; prepare the eventual disposition of the resolved ownership discussion #8 without inventing a code defect or sending unsolicited messages.

### M5: One auditable candidate and publishing path


Keep shared `.github/workflows/validate.yml` as the single reusable matrix used by CI, nightly and candidate workflows. Add an explicit required full-composition release gate so a broken union cannot publish. Validate a reviewed immutable commit, build the source archive first and derive the wheel from it, and test those exact archives in fresh minimal and full consumer environments. Produce machine-readable evidence binding source SHA, canonical version, artifact SHA256 values and workflow URL. Reject missing, extra, mismatched or stale release inputs.

Strengthen `pypi.yml` so validation is the default and only an explicit publication action can reach the OIDC job after all candidate gates succeed. Prevent concurrent publication for the same release. Require exact canonical version tag/source/workflow identity and main reachability; preserve prerelease consistency and the rule that upload consumes existing validated artifacts rather than rebuilding. Test release tooling with realistic positive and negative temporary Git repositories, including inherited Git environment isolation. Exercise hooks and actionlint for changed workflows.

Write a maintainer release runbook linked from `CONTRIBUTING.md` and `tools/README.md`: tool bootstrap, version/changelog preparation, validation-only dispatch, evidence review, GPU proof, tag/release identity, one explicit publish procedure, verification, retries and recovery. Explain immutable PyPI versions, no accidental re-upload or rebuild, and separate Pages deployment. Provide exact reviewed requirements for branch/tag protection, required validation, pypi reviewers/self-approval/bypass/tag policy, and PyPI trusted publisher owner `beartype`, repository `bearshape`, workflow `pypi.yml`, environment `pypi`. Do not apply these access changes or upload now.

### M6: Validate the final candidate and document its limits


Set candidate 0.1.0rc1 once changes are integrated and update CHANGELOG, installation/support guidance and the current handoff summary. Run Linux 3.11–3.14, macOS/Windows endpoints, all four static engines, configured backend/checker floors, coverage at the existing threshold, normal hooks/manual actionlint, docs/rendered snippets and the executed notebook. Build and normally install archives outside source checkouts. Run the final wheel on available CUDA hardware, capturing Python/CuPy/CUDA/device versions, source SHA and hashes. CPU skips and September H200 results do not constitute new GPU evidence. If a lane is unavailable, record that limit rather than claiming it passed.

Evaluate Python 3.15/free-threaded dependency availability as a follow-up compatibility decision; retain only proven support claims. Report release controls and private publisher verification as separate owner prerequisites. Present every PR with completed/pending checks and a proposed disposition. After explicit merge approval and passing checks, preserve reviewed heads in history, verify main and clean only clean merged worktrees. Never publish during this program.

## Concrete Steps


Run from each focused worktree root. Use uv 0.11.17 (the isolated audit environment at `/private/tmp/bearshape-audit-2026-10-11/venv310/bin/uv` currently provides it) and a worktree-specific environment. Keep logs under the main checkout's ignored `build/release-2026-10-11/` so worktree cleanup cannot erase evidence.

    uv sync --locked --python 3.11
    uv run --locked prek install
    uv run --locked pytest tests/ --ignore=tests/test_typecheck.py -n auto
    uv run --locked pytest tests/test_typecheck.py -q
    uv run --locked prek run -a
    uv run --locked prek run actionlint -a --stage manual

After M1 the endpoint tox names become `py311-bt0231-cpu` and `py314-bt0231-cpu`. Run floor environments listed by `uv run --locked tox list`; do not invent factors. Run tools/validate_runtime.py with the documented lane arguments. For archive proof:

    uv build --sdist
    uv build dist/bearshape-0.1.0rc1.tar.gz --wheel
    uv run --locked python tools/check_distribution.py dist/*.whl dist/*.tar.gz
    uv run --locked python tools/check_installed.py dist/*.whl dist/*.tar.gz --python 3.11
    uv run --locked python tools/check_installed.py dist/*.whl dist/*.tar.gz --python 3.14
    uv run --locked --only-group docs zensical build --clean
    uv run --locked --only-group docs python tools/check_docs.py
    uv run --locked python tools/check_notebook.py

Use fresh environments for minimal consumers. For upstream prototype testing invoke its isolated interpreter directly; `uv run --locked` would reinstall published beartype and invalidate that experiment. Record concrete PR URLs and revised commands as milestones complete.

## Validation and Acceptance


For every behavioral fix, a focused regression must fail on the original source and pass on the fix. Every existing named, anonymous, arithmetic, fixed and broadcast dimension, Scalar, Value, native backend alias, Like, scalar-like and Tree feature must remain covered by positive and negative cases. Root import must load none of NumPy/JAX/Torch/CuPy/optree. Static support means real accepted/rejected/inferred consumers for pyright, mypy, ty and pyrefly, not Any or skipped checks.

Full union acceptance means failed alternatives/expressions restore single, variadic and tree bindings; successful alternatives and earlier bindings survive; diagnostics do not mutate checks; exceptions/cancellation unwind; lazy references, sampling and object lifetimes remain correct. The 22-case suite and original probe must pass with a normally installable supported dependency. A locally patched upstream pass is evidence for the proposal only.

Release automation acceptance means validation-only cannot upload, any failed required lane or unresolved union contract prevents upload, source/tag/version and prerelease mismatches fail, and only identical tested artifacts enter the gated publisher. Administrative setup and private PyPI trust require separate verified evidence. Implementation completion is not publication readiness and publication is explicitly excluded.

## Idempotence and Recovery


Preserve main, existing unmerged branches and September evidence. Create matching feature worktrees, inspect status before edits, and commit plans before implementation. Re-run validators safely in fresh environments; do not overwrite release artifacts with different content under the same evidence name. Never force main, delete another contributor's work, or erase dirty worktrees. If upstream support remains unavailable, leave the failing gate and concrete proposal visible and finish independent work.

## Artifacts and Notes


Audit: `/Users/ale/Code/bearshape/build/audit-2026-10-11/AUDIT.txt`, with `evidence/` and `reproducers/`. Initial ordinary 0.23.1 tests: 1,101 passed with five CPU skip records per audited endpoint. Initial union tests: 20 failed, two passed. Current source and PR SHAs are recorded above. Future evidence belongs in `build/release-2026-10-11/` and focused plans with artifact hashes and URLs, excluding secrets.

## Interfaces and Dependencies


Public annotation syntax, direct `bearshape.claw` alias and current backend boundaries remain stable. `ShapeMemo.snapshot()`/`restore(token)` remain the state contract. The proposed upstream `__beartype_state__` getter is opt-in and returns shared snapshot-capable state; it must not import bearshape/backends or retain caller objects after checking. No new runtime dependency is planned. Retain uv 0.11, the four supported checkers, optree's default registry and the accepted native CuPy static limits. Git tools creating temporary repositories must use the existing `git_environment` helper to remove inherited local Git variables.

Revision note — 2026-10-11: Created the detailed program plan before implementation, incorporating audit A01–A15 and the owner's new baseline, Python floor and no-publication instruction.
