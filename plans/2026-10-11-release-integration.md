# Integrate and verify the next bearshape candidate


This living ExecPlan follows `PLANS.md` and M4/M6/M7 of `plans/2026-10-11-release-readiness.md`. Preserve the Progress, Surprises & Discoveries, Decision Log and Outcomes & Retrospective sections as execution proceeds.

## Purpose / Big Picture


Reviewers need a concrete combined candidate that preserves every focused PR's history and exposes any remaining release blockers. Integrate the Python 3.11/beartype 0.23.1 baseline, four audited correctness fixes, release pipeline and existing action/memo/union PRs in a separate branch; prepare 0.1.0rc1 and validate its exact archives. No merge into main, tag, release, upload or deployment is authorized by this integration.

## Progress


- [x] (2026-10-11) Created the integration branch from the validated baseline.
- [x] (2026-10-11) Commit plan and open draft PR before integrating implementations.
- [x] (2026-10-11) Merge focused heads and PRs #32/#34/#35, preserving ancestry and resolving conflicts surgically.
- [x] (2026-10-11) Set the independent candidate identity, update current readiness documentation and release notes.
- [x] (2026-10-11) Run combined source/checker/hooks/docs/notebook and installed-archive validation, plus hosted platform/floor lanes.
- [x] (2026-10-11) Run the final wheel on actual CUDA hardware; record versions/source/hashes and real results.
- [x] (2026-10-11) Validate the same final bearshape artifact with the refreshed upstream proposal, including transaction/lifetime/performance evidence.
- [x] (2026-10-11) Run validation-only release workflow; report the real published-0.23.1 contract failure explicitly.
- [x] (2026-10-11) Prepare all reviewed PR heads, evidence, external prerequisites and proposed dispositions for merge approval. Do not publish.

## Surprises & Discoveries


The refreshed local upstream proposal passes all 22 transaction cases on both Python endpoints, while published 0.23.1 fails 20. It is not a normal supported dependency yet. CPU skips do not substitute for GPU proof.

## Decision Log


Decision: Merge branch heads into this integration branch, not cherry-pick or squash them. Rationale: preserve reviewed contributors' changes and permit explicit reachability checks before any approved main merge. Author/date: Codex, 2026-10-11.

Decision: Keep release readiness withheld while preparing candidate 0.1.0rc1. Rationale: the user requested implementation with no publishing, and unavailable supported union integration remains a real blocker. Author/date: Codex, 2026-10-11.

## Outcomes & Retrospective


Independent implementation and ordinary candidate validation are complete. Supported union integration remains the release blocker, with a tested local upstream proposal prepared for review. No main merge, release tag, upload, deployment, access change or upstream message has occurred. Merge and publication readiness are separate outstanding decisions.

## Context and Orientation


The parent program plan records all audit findings and original heads. New focused branches are `codex/python311-beartype0231`, `codex/nested-value`, `codex/converter-validation`, `codex/variadic-broadcast`, `codex/tree-ellipsis` and `codex/release-pipeline`. Existing #32 is `dependabot/github_actions/github-actions-9a5dc421c7`; #35 is `codex/memo-discovery-performance`; #34 is `codex/union-transactions`, now refreshed against the new baseline. Each already has its own reviewable scope and tests.

The upstream proposal port is commit d0fe6e67a5ab693acb263e4bb0e1eb7131dc3fba in `/private/tmp/beartype-union-0231`, based on released v0.23.1. Its durable patch is in the main checkout's `build/release-2026-10-11/`; never apply it to installed library files or pretend the published version contains it.

## Plan of Work


Open the plan PR, then merge each focused head using ordinary Git merges. Resolve changelog conflicts by retaining all independent entries, keep current beartype organization identity and baseline decisions, and correct action version comments to the verified pinned tags. Preserve #35's frame filter and #34's adapter/tests. Record every source head and confirm it is an ancestor of integration HEAD.

Set pyproject version to 0.1.0rc1 and refresh the lock/current candidate filenames and agent guidance. Preserve historical evidence and the published-0.23.1 union blocker. Run required validation and build source then wheel into a clean directory. Normally install copied archive consumers on both endpoints, and validate the final CuPy artifact. Compare matched benchmark runs with the frame filter and upstream proposal separated. Use isolated upstream environments directly rather than uv run, which would restore published dependencies.

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

## Completed evidence, 11 October 2026


Artifact-producing source is f7d54d5e9f68e4ef63cb727cff625d885281b0a7. Subsequent
documentation follow-up also corrects the changelog's obsolete Python endpoint;
the final source archive identity is recorded separately below. Durable local evidence is
`/Users/ale/Code/bearshape/build/release-2026-10-11/` and survives worktree cleanup.
The wheel is bearshape-0.1.0rc1-py3-none-any.whl, SHA256
007d1905c677057240eaa2569b417325a7258fb0b4c68e7f2e19e0c6846b6231. The source archive
is bearshape-0.1.0rc1.tar.gz, SHA256
2096217b3ebb94503e2b9cd80775a606d931f89248c72cfdfc4643d805aeddf2.

Source Python 3.11 validation passed 1,142 cases with five existing CPU skip
records and 92.05% coverage with branch measurement enabled. Normal installed-wheel consumers copied from
the sdist, without src, passed 1,142 cases on EACH Python 3.11.15 and 3.14.5,
including the four checker harnesses. The five skips are absent CuPy and four
macOS extended-precision dtype cases. Fresh minimal consumers passed on both
endpoints with zero optional imports, including backend-free broadcasting and
canonical /tmp environment paths. Normal hooks and manual actionlint passed.
The rendered docs check covered 94 Python snippets; all 29 tour notebook cells
executed. Logs are evidence/integration-all311.log, installed311.log,
installed314.log, minimal-3.11.log, minimal-3.14.log, integration-docs.log,
integration-notebook311.log and integration-hooks-final.log.

Hosted CI run 38132351427 passed every shared lane: Linux 3.11–3.14,
macOS/Windows 3.11 and 3.14, four static checkers on every interpreter, the twelve
configured backend/checker floor lanes, docs, endpoint notebooks, distribution,
minimal and normal installed-wheel consumers. See
https://github.com/beartype/bearshape/actions/runs/38132351427.

Validation-only release run 38132526795 used the full artifact source SHA with
publish=false. Resolve and all shared validation jobs passed. The two full-
composition jobs failed for the real N=2 binding leak, and evidence/publication
were skipped. Downloaded candidate-distributions hashes exactly match the local
artifacts above. This is successful verification of the blocker, NOT successful
release acceptance. Run 38132402776 had previously failed at checkout because an
abbreviated SHA was supplied; the runbook now requires all 40 characters. See
https://github.com/beartype/bearshape/actions/runs/38132526795 and the saved
validation-only-run.json / validation-only-union-blocked.log.

The exact wheel passed all 95 CuPy tests on Python 3.11.15 and 3.14.5 with
beartype 0.23.1, NumPy 2.4.6, CuPy 14.2.0, optree 0.19.1 and CUDA 12.9.
Together with shared dtype tests each endpoint had 193 passes and 28 unrelated
absent Torch/JAX skips. These results do not establish multi-device support or
native CuPy static inference. Machine-specific operational details are excluded
from project documentation.

The upstream port d0fe6e67a5ab693acb263e4bb0e1eb7131dc3fba is based on released
v0.23.1 f85b67d8b0b6bd9c910bd97f0d2d417c4550b038. Upstream a00_unit passed
449/15 skipped on 3.11 and 457/7 skipped on 3.14. The initial 3.11 run
without optional scientific backends had 446 passes and 18 skips; the final
normally installed wheel run includes those available backend cases. Upstream pyright passed. With the normally
installed proposal and the exact final bearshape wheel, copied consumers passed
1,164 cases on EACH endpoint, including all 22 transaction cases and four
checker engines. The original probe passed. Protocol tests include 600
independent reference cases and copied-context/lifetime regressions.
The proposal wheel SHA256 is
3cc168846f71053cc975d0e0fb202dcfa38a100e49b7d1d50afb6b7d98664a03; normal reinstalls
of this exact wheel passed the original probe and 22 cases on both endpoints.
Its unchanged upstream 0.23.1 version string is NOT the released 0.23.1 artifact.
The durable patch and UPSTREAM-PROPOSAL.txt are prepared but have not been sent.

Matched benchmarks use 20,000 calls per repeat and seven raw repeats on macOS
arm64, both endpoint interpreters, NumPy 2.4.6 and the same final bearshape wheel.
A separate normally installed counterfactual wheel reverses only the memo.py
change from 344d390 to isolate PR #35. Strict medians improved from 13.706 to
12.506 microseconds on 3.11 and 17.599 to 12.604 on 3.14. Separately, adding the
upstream transaction proposal changes strict medians from 12.506 to 16.180 and
12.604 to 16.032; correct fallback unions take 25.163 and 25.261 microseconds.
Stateless native checks remain about 0.1 microseconds, while nested ordinary
forward references rise from 0.684 to 1.139 and 0.542 to 0.893. Keep this remaining
cost explicit. Incorrect union baselines are labelled incorrect, not timed as
successful calls. Raw samples, correctness flags, benchmark/source and artifact
hashes are in evidence/perf-{unfiltered,released,prototype}{311,314}.json.
No timing threshold was introduced into CI.

Python 3.15 availability was evaluated using uv 0.11.17's interpreter inventory
and wheel-only resolution for the locked scientific stack on macOS arm64. The
locked NumPy 2.4.6 has no usable wheel there; no 3.15 compatibility claim follows.
Free-threaded builds exist in the inventory, but the required full backend,
checker and concurrency/lifetime evidence is absent, so this is outside the
claimed 3.11–3.14 matrix. See python-availability.json and python315-resolution.log.

PR disposition: #32 action updates, #35 memo filtering and #38–#44 focused plan,
baseline, fixes and pipeline are reviewable in the combined history. #34 retains
the supported-upstream adoption blocker. #45 is the integration/evidence review
packet and remains a draft pending that decision. Do not close release request
#37 before publication; ownership discussion #8 can be closed administratively
later. No unsolicited comments have been sent. Main and all unmerged worktrees
are preserved for owner review.

Revision note — 2026-10-11: Replaced queued validation with completed local,
hosted, archive, GPU and prototype evidence; recorded performance costs, the
failed-closed release run and remaining external work. Later evidence-only commits do not authorize any publication.

## Final archive and review follow-up


Source 26b293cf6f7db9bbd928f6d0d2fda7c8bff93ce8 produces the final review archives
under `build/release-2026-10-11/final-dist/`. The wheel SHA256 remains
007d1905c677057240eaa2569b417325a7258fb0b4c68e7f2e19e0c6846b6231; the source
archive SHA256 is now
d75180399f300dde9bb947012a65e2610f6a4f055cf956b253b8a28dd7f793d0.
Comparing every source-archive member proves only CHANGELOG.md changed from the
first artifact set; it corrects an obsolete Python 3.10 endpoint. The wheel is
byte-for-byte identical. No new device execution was needed or performed.

The final source's ordinary hosted CI passed all 34 jobs:
https://github.com/beartype/bearshape/actions/runs/38133983895.
Validation-only run https://github.com/beartype/bearshape/actions/runs/38134009706
passed resolve and all shared lanes, failed only the two real composition checks,
and skipped evidence/upload. Its downloaded archives match the final local
hashes. Saved evidence files are final-integration-ci-run.json,
final-validation-only-run.json and final-validation-only-union-blocked.log.

All four runtime-fix PRs have been refreshed against the final #39 baseline and
are independently mergeable, with all 34 checks passing per focused head. Their
baseline-merge commits preserve identical trees to their earlier implementation
heads. The final two ancestry-only integration merges were guarded by complete
tree equality and ancestor checks; they do not change any candidate files.
Every original and latest reviewed head is retained. #35 and #38–#44 are ready
for owner review; #34 and #45 remain drafts with the supported-upstream decision
explicit. Main is unchanged. No release or publication has occurred.

Revision note — 2026-10-11: Recorded the final source-archive hash, fully finished
hosted runs and independent PR conflict resolutions. Machine-specific operating
instructions were removed from current review documentation; package evidence
is retained without personal infrastructure identifiers.
