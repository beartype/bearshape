# Execution plans and historical evidence

Use [CONTRIBUTING.md](../CONTRIBUTING.md) for current development commands,
[AGENTS.md](../AGENTS.md) for agent rules and [PLANS.md](../PLANS.md) to write a
new plan. The [handoff](../docs/maintainers/production-readiness.md) owns current
release status; [releasing.md](../docs/maintainers/releasing.md) owns publishing
prerequisites. A historical plan is not a current installation recipe.

## Latest documentation audit

[Documentation alignment](2026-10-12-docs-alignment.md) covers user, contributor,
agent and maintainer guidance against the runtime baseline at a475c9b. The owner
approved review and merge on 12 October 2026;
[PR #58](https://github.com/beartype/bearshape/pull/58) records the reviewed head,
validation and merge status. Publication and upstream acceptance remain separate.

## Completed implementation and remaining release work

The reviewed candidate/audit stack through #55 merged at 28e8858. Optimizations
#56/#57 merged at a475c9b on 12 October 2026, with reviewed commits preserved and
main validation successful. Their temporary worktrees and branches were cleaned
up after saving evidence. The implementation and merge phases are complete;
publication remains withheld for supported native-union integration, final
artifact CUDA evidence and repository/PyPI controls. CuPy's limited static
protocol is an accepted boundary, not a pending policy choice.

Plans below retain original dates, sources, test totals, pending-review wording
and experiments. Later decisions here and in the handoff supersede those older
status statements. Their local `build/` and temporary-checkout paths describe
evidence locations on the original validation host; use committed reports,
linked CI artifacts and documented drivers to reproduce results elsewhere.

## Plan inventory

- [2026-05-28-baseline-audit: Baseline audit before bearshape rename](2026-05-28-baseline-audit.md)
- [2026-05-28-hook-ci-hygiene: Hook and CI hygiene before bearshape rename](2026-05-28-hook-ci-hygiene.md)
- [2026-05-29-bearshape-rename: Rename Project Identity to bearshape](2026-05-29-bearshape-rename.md)
- [2026-09-07-typing-ci-floor: Keep typing checks aligned with supported Python versions](2026-09-07-typing-ci-floor.md)
- [2026-09-08-action-runtimes: Use supported runtimes for artifact and Pages actions](2026-09-08-action-runtimes.md)
- [2026-09-08-agent-workflow: Align agent guidance and merge the approved production work](2026-09-08-agent-workflow.md)
- [2026-09-08-backend-conversion: Validate Like inputs with the target backend's converter](2026-09-08-backend-conversion.md)
- [2026-09-08-checker-conformance: Verify useful public typing with four checker engines](2026-09-08-checker-conformance.md)
- [2026-09-08-ci-validation: Make CI reproduce the release support contract](2026-09-08-ci-validation.md)
- [2026-09-08-claw-caller: Instrument the actual caller package through bearshape.claw](2026-09-08-claw-caller.md)
- [2026-09-08-cupy-runtime: Verify the corrected CuPy runtime on CUDA](2026-09-08-cupy-runtime.md)
- [2026-09-08-distribution-integrity: Ship complete, testable source and wheel distributions](2026-09-08-distribution-integrity.md)
- [2026-09-08-docs-contract: Repair rendered documentation and executable examples](2026-09-08-docs-contract.md)
- [2026-09-08-framework-validation: Prove framework transformations and minimal runtime imports](2026-09-08-framework-validation.md)
- [2026-09-08-handoff-evidence: Prepare the production review and ownership handoff evidence](2026-09-08-handoff-evidence.md)
- [2026-09-08-installed-consumers: Prove the normally installed candidate artifact](2026-09-08-installed-consumers.md)
- [2026-09-08-memo-discovery-performance: Reduce the cost of locating the active checking frame](2026-09-08-memo-discovery-performance.md)
- [2026-09-08-production-readiness: Make bearshape ready for a verified beartype 0.23.0rc0 release](2026-09-08-production-readiness.md)
- [2026-09-08-publication-gate: Publish only the exact validated release artifacts](2026-09-08-publication-gate.md)
- [2026-09-08-rc0-compat: Install and validate the 0.1.0rc0 candidate with exact beartype rc0](2026-09-08-rc0-compat.md)
- [2026-09-08-rc0-integration: Validate the combined release candidate](2026-09-08-rc0-integration.md)
- [2026-09-08-release-candidate: Validate the full independent PR set together](2026-09-08-release-candidate.md)
- [2026-09-08-static-like-inputs: Make static Like inputs reflect ordinary backend conversion](2026-09-08-static-like-inputs.md)
- [2026-09-08-static-tree-containers: Give ordinary Tree consumers a useful static type](2026-09-08-static-tree-containers.md)
- [2026-09-08-union-transactions: Roll back failed native union alternatives](2026-09-08-union-transactions.md)
- [2026-09-08-validation-lifetime: Scope validation state to the check that owns it](2026-09-08-validation-lifetime.md)
- [2026-09-10-ownership-transfer: Restore bearshape after transfer to beartype](2026-09-10-ownership-transfer.md)
- [2026-10-11-audit-followup: Close the combined candidate audit in focused changes](2026-10-11-audit-followup.md)
- [2026-10-11-converter-validation: Reject malformed custom Like converter results](2026-10-11-converter-validation.md)
- [2026-10-11-dtype-normalization: Normalize builtin dtypes without retaining checked objects](2026-10-11-dtype-normalization.md)
- [2026-10-11-nested-value: Preserve scope in nested Value arithmetic](2026-10-11-nested-value.md)
- [2026-10-11-python311-beartype0231: Adopt Python 3.11 and beartype 0.23.1 coherently](2026-10-11-python311-beartype0231.md)
- [2026-10-11-release-integration: Integrate and verify the next bearshape candidate](2026-10-11-release-integration.md)
- [2026-10-11-release-pipeline: Validate immutable candidates and publish only reviewed artifacts](2026-10-11-release-pipeline.md)
- [2026-10-11-release-readiness: Prepare bearshape for Python 3.11 and released beartype](2026-10-11-release-readiness.md)
- [2026-10-11-shape-preparation: Prepare invariant shape traversal once per annotation](2026-10-11-shape-preparation.md)
- [2026-10-11-tree-ellipsis: Reject invalid Tree ellipsis syntax](2026-10-11-tree-ellipsis.md)
- [2026-10-11-union-ordinary-performance: Reduce ordinary checking overhead without weakening rollback](2026-10-11-union-ordinary-performance.md)
- [2026-10-11-union-scope-correctness: Preserve state across internal alias checks](2026-10-11-union-scope-correctness.md)
- [2026-10-11-variadic-broadcast: Broadcast custom array shapes without NumPy](2026-10-11-variadic-broadcast.md)
