# Validate immutable candidates and publish only reviewed artifacts

> Historical execution record. Versions, commands and pending actions below
> describe this work at the time. Use the [plan index](README.md),
> [current contributor guide](../CONTRIBUTING.md) and
> [current handoff](../docs/maintainers/production-readiness.md) for today's
> workflow, merge status and release prerequisites.


This living ExecPlan follows `PLANS.md` and milestone M5 of `plans/2026-10-11-release-readiness.md`. It is stacked on baseline PR #39. Keep Progress, Surprises & Discoveries, Decision Log and Outcomes & Retrospective current.

## Purpose / Big Picture


Maintainers need a repeatable route from a reviewed commit to tested wheel/source archives, then a separately authorized publication of the exact same bytes. Validation-only runs must never upload. A failed full-composition contract must block release even when ordinary CPU tests pass. The owner requested clean publishing automation, associated CI and developer documentation, and explicitly prohibited publishing now.

## Progress


- [x] (2026-10-11) Reviewed current source/tag checks, reusable CI, archive validation and publishing workflow.
- [x] (2026-10-11) Commit the plan and open a draft PR before implementation.
- [x] (2026-10-11) Add explicit release-contract validation, archive evidence verification and publication concurrency.
- [x] (2026-10-11) Test positive/negative release inputs with disposable repositories and artifacts; run real hooks/actionlint.
- [x] (2026-10-11) Write developer/maintainer instructions, build and inspect rendered documentation, and prepare the administrative prerequisite list.
- [x] (2026-10-11) Exercised validation-only run 38132526795 against full source SHA f7d54d5e9f68e4ef63cb727cff625d885281b0a7: all shared lanes passed, both full-composition gates failed on the real union defect, and evidence/upload were skipped. This proves blocking behavior, not release acceptance.

## Surprises & Discoveries


The existing workflow already builds a source archive before its wheel and downloads the same artifacts for publication. Preserve this useful foundation. However, the separate union reproducer is not a release gate; released 0.23.1 still fails it. GitHub main/tag protections and pypi environment reviewers are absent, and private PyPI trust remains unverified. YAML changes cannot establish those account settings.

## Decision Log


Decision: Keep one reusable baseline matrix and add an explicit release-contract gate to candidate/publication validation. Rationale: do not confuse ordinary dependency compatibility with full native union correctness; the current published baseline must remain testable while releases fail closed. Author/date: Codex, 2026-10-11.

Decision: Retain trusted publishing with OIDC and no upload token. Verify artifact filenames, hashes, version, source SHA and originating workflow immediately before the upload job. Rationale: approval should identify exact reviewed bytes, and publication must never rebuild. Author/date: Codex, 2026-10-11.

Decision: Keep publication an explicit event after review and serialize publication attempts for a version. Do not create a tag/release, upload, deploy Pages or change access controls in this task. Rationale: explicit owner restriction and repository approval policy. Author/date: owner/Codex, 2026-10-11.

## Outcomes & Retrospective


Implemented in PR #44. All 34 release identity/evidence tests pass. Normal hooks and manual actionlint pass; the docs build/render checks pass, and the new runbook navigation/headings were inspected. Both CLI modes passed against the real audited wheel/source archives in a clean directory. The initial CLI run correctly rejected uv build's extra .gitignore; downloaded GitHub distribution artifacts omit hidden files. The publisher receives exactly the two archives. Readiness remains blocked by supported upstream union integration and external release prerequisites; a working validation pipeline should expose those blockers rather than claim readiness.

## Context and Orientation


`.github/workflows/validate.yml` is called by CI, nightly and pypi workflows. It requires quality, CPU runtime, four checker engines, floor environments, docs, notebook, distribution, minimal and installed-wheel jobs. `tools/check_release.py` validates canonical versions, tag/source/workflow identity, prerelease status and ancestry on origin/main. `tools/check_distribution.py` checks matching wheel/sdist contents, license, typing marker, metadata and SHA256 hashes. `tools/check_installed.py` normally installs a wheel and executes copied archive consumers outside source. `tools/probe_union.py` demonstrates the still-failing native union case.

The existing `pypi.yml` has resolve, shared validation, evidence and environment-gated publishing jobs. Only publishing receives `id-token: write`; the pypi environment is the administrative approval boundary. The published package remains 0.0.1; future candidate identity is independent of beartype. Existing release tests use real temporary Git histories and the `git_environment` helper to avoid inherited hook variables.

## Plan of Work


Add a required contract job to the release workflow on Python 3.11/3.14. It runs the original union probe and the expanded transaction suite when the adapter branch is integrated; absent required inputs must fail rather than silently skip. Keep it separate from ordinary baseline compatibility and make evidence/upload depend on success. Expose its current failure clearly in the developer runbook. Once supported upstream adoption is available, move the cases into mandatory source and installed-archive tests as described by M3.

Extract the evidence record/verification logic from inline workflow Python into a small maintained tool with a record mode and a verify mode. Reuse `check_distribution` for archive contents. Bind a manifest to the source SHA, project version and workflow run URL; verification rejects altered bytes, extra/missing archives, filename traversal and identity mismatches. The publisher downloads only this run's candidate and evidence artifacts, verifies them, then invokes the pinned PyPI action without rebuilding. Keep permissions least-privileged and artifact upload failures fatal. Add concurrency without cancelling an in-flight publication.

Extend realistic release tests for validation-only source identity and artifact manifest failure cases. Preserve canonical tag/version/event/ancestry checks and Git environment isolation. Add a release runbook under `docs/maintainers/`, link it from CONTRIBUTING/tools documentation, and include it in docs navigation. Document bootstrap, candidate preparation, validation-only dispatch, CPU/checker/GPU evidence, exact-artifact review, explicit future publish, retry/recovery and separate docs deployment. List precise required administrative settings and PyPI trust identity; do not apply them now.

## Concrete Steps


From this worktree with uv 0.11.17 on PATH:

    uv sync --locked
    uv run --locked prek install
    uv run --locked pytest tests/test_release.py -n 0
    uv run --locked prek run -a
    uv run --locked prek run actionlint -a --stage manual
    uv run --locked --only-group docs zensical build --clean
    uv run --locked --only-group docs python tools/check_docs.py

Build source then wheel and test evidence against real archives. Run a validation-only workflow only after the integration head exists; never pass publish=true in this task. Its union job is expected to report a real failure with published beartype 0.23.1, which is a release block rather than successful acceptance.

## Validation and Acceptance


A validation-only request cannot upload. A wrong/missing tag, wrong version/source/workflow, unmerged source, malformed prerelease flag, failed union contract or failed shared lane prevents upload. A changed/missing/extra archive or mismatched manifest is rejected. Only the exact validated wheel and source archive reach OIDC publication. Real hooks and actionlint pass; developer commands and rendered docs are checked. Private PyPI trust, approved GPU evidence and administrative controls remain explicitly separate prerequisites.

## Idempotence and Recovery


Preserve previous artifacts and evidence; PyPI versions are immutable. Retry validation with fresh artifact names/runs, never overwrite a published version. Use dry validation by default. Do not store credentials or add tokens. Use the existing Git environment helper in all cross-repository subprocesses. Keep logs under the main checkout's ignored `build/release-2026-10-11/evidence/`.

## Artifacts and Notes


The October audit contains the current GitHub control snapshots and exact baseline failures. Append source commits, test results, hashes and workflow URLs here as implementation proceeds. Successful local tests do not prove private publisher settings or a hosted run.

## Interfaces and Dependencies


Use standard-library release tooling, existing check_distribution/git_environment helpers, pinned GitHub actions and uv 0.11.17. Trusted publisher identity must be owner beartype, repository bearshape, workflow pypi.yml, environment pypi. No runtime bearshape API changes or new runtime dependencies belong in this PR.

Revision note — 2026-10-11: Created the focused automation/runbook plan before implementation, preserving the explicit no-publication boundary.

Revision note — 2026-10-11: Recorded implementation and local evidence; hosted validation-only integration remains pending and full composition remains blocked by published upstream.

Revision note — 2026-10-11: The first dispatch used an abbreviated SHA and failed
at checkout (run 38132402776); rerunning with the full SHA exercised the intended
contract failure (run 38132526795). The runbook now makes this requirement
explicit. Its downloaded archives exactly match the locally tested and GPU-tested
wheel/source hashes. The owner reports the PyPI project in their personal account;
that ownership arrangement is compatible with trusted publishing. The GitHub
reviewer choice and private publisher verification remain pending. No access
settings or publishing actions were changed.
