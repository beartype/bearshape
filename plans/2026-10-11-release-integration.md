# Integrate and verify the next bearshape candidate


This living ExecPlan follows `PLANS.md` and M4/M6/M7 of `plans/2026-10-11-release-readiness.md`. Preserve the Progress, Surprises & Discoveries, Decision Log and Outcomes & Retrospective sections as execution proceeds.

## Purpose / Big Picture


Reviewers need a concrete combined candidate that preserves every focused PR's history and exposes any remaining release blockers. Integrate the Python 3.11/beartype 0.23.1 baseline, four audited correctness fixes, release pipeline and existing action/memo/union PRs in a separate branch; prepare 0.1.0rc1 and validate its exact archives. No merge into main, tag, release, upload or deployment is authorized by this integration.

## Progress


- [x] (2026-10-11) Created the integration branch from the validated baseline; confirmed H200 CUDA hardware is reachable.
- [x] (2026-10-11) Commit plan and open draft PR before integrating implementations.
- [x] (2026-10-11) Merge focused heads and PRs #32/#34/#35, preserving ancestry and resolving conflicts surgically.
- [x] (2026-10-11) Set the independent candidate identity, update current readiness documentation and release notes.
- [ ] Run combined source/checker/hooks/docs/notebook and installed-archive validation, plus hosted platform/floor lanes.
- [ ] Run the final wheel on actual CUDA hardware; record versions/source/hashes and real results.
- [ ] Validate the same final bearshape artifact with the refreshed upstream proposal, including transaction/lifetime/performance evidence.
- [ ] Run validation-only release workflow; report the real published-0.23.1 contract failure explicitly.
- [ ] Present all reviewed PR heads, evidence, external prerequisites and proposed dispositions for merge approval. Do not publish.

## Surprises & Discoveries


The refreshed local upstream proposal passes all 22 transaction cases on both Python endpoints, while published 0.23.1 fails 20. It is not a normal supported dependency yet. CPU skips do not substitute for GPU proof; the available H200 host reports NVIDIA driver 575.57.08.

## Decision Log


Decision: Merge branch heads into this integration branch, not cherry-pick or squash them. Rationale: preserve reviewed contributors' changes and permit explicit reachability checks before any approved main merge. Author/date: Codex, 2026-10-11.

Decision: Keep release readiness withheld while preparing candidate 0.1.0rc1. Rationale: the user requested implementation with no publishing, and unavailable supported union integration remains a real blocker. Author/date: Codex, 2026-10-11.

## Outcomes & Retrospective


Integration and candidate validation pending. Implementation, hosted checks, merge completion and publication readiness will be reported separately.

## Context and Orientation


The parent program plan records all audit findings and original heads. New focused branches are `codex/python311-beartype0231`, `codex/nested-value`, `codex/converter-validation`, `codex/variadic-broadcast`, `codex/tree-ellipsis` and `codex/release-pipeline`. Existing #32 is `dependabot/github_actions/github-actions-9a5dc421c7`; #35 is `codex/memo-discovery-performance`; #34 is `codex/union-transactions`, now refreshed against the new baseline. Each already has its own reviewable scope and tests.

The upstream proposal port is commit d0fe6e67a5ab693acb263e4bb0e1eb7131dc3fba in `/private/tmp/beartype-union-0231`, based on released v0.23.1. Its durable patch is in the main checkout's `build/release-2026-10-11/`; never apply it to installed library files or pretend the published version contains it.

## Plan of Work


Open the plan PR, then merge each focused head using ordinary Git merges. Resolve changelog conflicts by retaining all independent entries, keep current beartype organization identity and baseline decisions, and correct action version comments to the verified pinned tags. Preserve #35's frame filter and #34's adapter/tests. Record every source head and confirm it is an ancestor of integration HEAD.

Set pyproject version to 0.1.0rc1 and refresh the lock/current candidate filenames and agent guidance. Preserve historical evidence and the published-0.23.1 union blocker. Run required validation and build source then wheel into a clean directory. Normally install copied archive consumers on both endpoints, and execute the final artifact on H200 with CuPy. Compare matched benchmark runs with the frame filter and upstream proposal separated. Use isolated upstream environments directly rather than uv run, which would restore published dependencies.

Update the current handoff with exact source/version/hash evidence and links to checks. Dispatch the integration branch's release workflow with publish=false; it must report the full-composition failure while upload stays skipped. Do not submit upstream contact, apply administrative controls, merge main or publish without the appropriate separate approval.

## Concrete Steps


From this worktree, use uv 0.11.17 and a worktree-specific environment:

    uv sync --locked
    uv run --locked prek install
    uv run --locked pytest tests/ --ignore=tests/test_typecheck.py -n auto
    uv run --locked pytest tests/test_typecheck.py -q
    uv run --locked prek run -a
    uv run --locked prek run actionlint -a --stage manual
    uv run --locked --only-group docs zensical build --clean
    uv run --locked --only-group docs python tools/check_docs.py
    uv run --locked python tools/check_notebook.py
    uv build --sdist
    uv build dist/bearshape-0.1.0rc1.tar.gz --wheel
    uv run --locked python tools/check_installed.py dist/*.whl dist/*.tar.gz --python 3.11
    uv run --locked python tools/check_installed.py dist/*.whl dist/*.tar.gz --python 3.14

Use the source archive's copied tests on CUDA with the same wheel; capture its SHA256 and actual imported package origin. Record concrete remote commands and hosted run URLs after execution.

## Validation and Acceptance


Every reviewed head is reachable. Ordinary source, static consumers, platform/backend floors, hooks, docs/notebook and normal archives pass without weakened negative tests or coverage. Changed custom broadcasting passes without optional imports. GPU evidence identifies the exact wheel and real CUDA execution. Prototype transaction cases pass with the port, and published dependency failures remain explicit. Publication is skipped. This is an implementation review packet, not a claim that private PyPI trust or upstream availability is complete.

## Idempotence and Recovery


Never force main or alter existing evidence. Preserve all unmerged worktrees and clean up only after approval, successful merge and ancestry verification. Keep source and prototype environments separate. Store logs/artifacts under the main checkout's ignored build directory, which survives managed worktree cleanup. No release tag or upload is created.

## Artifacts and Notes


All evidence belongs under `/Users/ale/Code/bearshape/build/release-2026-10-11/`. Record exact branch heads, commands, test counts, artifact hashes, backend/device versions and hosted URLs; distinguish local and queued checks.

## Interfaces and Dependencies


Preserve all public annotation syntax, memo ownership and backend boundaries. Baseline is Python >=3.11, beartype >=0.23.1,<0.24 with exact 0.23.1 validation; supported matrix initially ends at 3.14. Full composition still requires a future supported upstream state hook. Publishing uses exact tested archives and OIDC, with separate owner-controlled prerequisites.

Revision note — 2026-10-11: Created integration and final-evidence plan before combining focused changes.

Revision note — 2026-10-11: Integrated #32/#34/#35 and #39–#44, retained both independently appended test groups, corrected action pin comments and prepared unpublished 0.1.0rc1. All focused heads are retained as merge parents. Final validation is now running.
