# Repository validation tools

Run these tools from the repository root with the locked uv environment unless
an isolated consumer is specified. `CONTRIBUTING.md` owns the routine workflow;
`AGENTS.md` owns agent instructions. These are repository tools, not public
bearshape APIs or an additional agent framework.

## Environment and static checks

`uv run --locked python tools/validate_runtime.py cpu` verifies exact beartype
0.23.1, all four expected CPU backends and a CPU-only Torch build. It prints
versions and import paths. A backend tox name, such as `py311-bt0231-numpy22`,
selects its expected backend. This is a CPU preflight, not a CUDA or full
behavioral test.

Only the separate dependency canary uses `--latest-compatible`, which checks
beartype against the installed bearshape metadata. The default still enforces
exact 0.23.1; do not pass the canary flag to release acceptance. Nightly
upgrades only runtime/backend packages in its disposable lock, keeps the
maintained checker versions, runs runtime and all four consumers, and uploads
the resolved lock, versions, source SHA and results. Canary failures need
review; they do not silently update the committed lock or authorize release.

`uv run --locked python tools/validate_tox_env.py py311-bt0231-numpy22` checks
the factor vocabulary. It does not prove that a dependency combination is
installable. Use `uv run --locked tox list` for the maintained matrix.

`uv run --locked pytest tests/test_typecheck.py -q` is the four-checker entry
point. It checks source and positive consumers, then matches deliberate errors
by file, line and category. The harness gives Pyrefly the explicit consumer root
so cross-file fixtures resolve both in source and copied archive consumers.
Missing engines or crashes fail. Tox selects one checker through its explicit
factor; ordinary runs require all four. Keep each Python target paired with its
own interpreter and compatible dependency stubs.

## Coverage reports

Follow the [coverage command](../CONTRIBUTING.md#coverage-reports) to generate
`build/coverage/coverage.json`, `coverage.xml` and `htmlcov/` from the runtime
suite. JSON includes line and branch totals; HTML identifies uncovered source
lines. The shared CI workflow retains these files in `coverage-<os>-py<version>`
artifacts for seven days, associated with that run's source commit. The README
badge shows the enforced 90% floor. CPU reports do not establish CUDA coverage,
and the checker suite runs separately.

## Documentation and notebook

```bash
uv run --locked --only-group docs zensical build --clean
uv run --locked --only-group docs python tools/check_docs.py
uv run --locked python tools/check_notebook.py
```

`check_docs.py` needs the freshly built `site/`. It verifies table rows,
admonitions, the favicon and Python 3.11 snippet syntax. It does not execute
those snippets; `tests/test_examples.py` exercises selected real consumers.
Update expected rendered counts deliberately when changing page structure. Also
execute changed runnable snippets (including intended rejections) and inspect
affected pages. Examples requiring a real package or user-defined class need
their consumer fixtures; CUDA-only examples require separate hardware. Review
local links, source-versus-published version notices and API signatures when
changing guides; syntax checks cannot establish those facts.

`check_notebook.py` executes `examples/bearshape_tour.ipynb` in a fresh kernel
using the invoking interpreter, installed bearshape, NumPy and the notebook
group. It writes `build/bearshape_tour-<python>-executed.ipynb`; it does not
edit the source notebook or rely on saved outputs. CI runs both Python
endpoints.

## Release distributions

Build the sdist first, then its wheel as described in `CONTRIBUTING.md`.

```bash
uv run --locked python tools/check_distribution.py \
  dist/bearshape-0.1.0rc1-py3-none-any.whl dist/bearshape-0.1.0rc1.tar.gz
uv run --locked python tools/check_installed.py \
  dist/bearshape-0.1.0rc1-py3-none-any.whl dist/bearshape-0.1.0rc1.tar.gz \
  --python 3.11
```

Use the actual project version in filenames. `check_distribution.py` reads both
archives, verifies metadata/license/typing markers and matching package files,
and prints SHA256 hashes. It does not install or execute the package.

`check_installed.py` validates the pair, exports dependencies from the archive's
own lockfile, creates a temporary environment and installs the wheel normally
with exact beartype. It runs copied runtime and four-checker tests outside the
checkout with no `src` directory, then removes the temporary environment. It
requires uv, dependency access and the requested managed Python. Repeat at
Python 3.14. This is a CPU consumer check; CuPy is tested separately on CUDA.

`smoke_minimal.py` requires a fresh venv containing only the normally installed
wheel and declared runtime dependencies. Run its Python with `-I` and the
absolute script path, as in the shared workflow. It checks root import
isolation, custom-array parameters/returns and module origin. Do not run it in
the normal development venv: installed optional backends must cause it to fail.

`check_release.py` is the release workflow's identity check, not a standalone
publisher. It reads `PROJECT_VERSION`, `RELEASE_REF`, `PUBLISH` and GitHub
event, ref, workflow-SHA and output variables from `pypi.yml`. It verifies
canonical version/tag/history and event consistency for publication. Its Git
subprocesses clear hook-local repository variables. Test it through
`uv run --locked pytest tests/test_release.py -q`; the tests create disposable
real Git histories. Validation-only dispatch, publication and environment
requirements are documented in `CONTRIBUTING.md`.

## Open upstream integration and performance

```bash
uv run --locked python tools/probe_union.py
uv run --locked python tools/benchmark_runtime.py --calls 10000 --repeats 5
```

`tools/upstream/README.md` records the refreshed local upstream proposal and its
integration suite. The protocol is absent from published 0.23.1.

`probe_union.py` is a standalone release-blocker reproducer. With released
beartype 0.23.1 it prints versions and fails on a valid native composite-union
call: a failed alternative leaves a dimension binding behind. This failure is
expected evidence of an unresolved defect, not a passing test or xfail. To
evaluate an actual later upstream candidate, install it and bearshape normally
in a separate environment and invoke the probe there. Do not change the
development lock merely to try an upstream revision. A future fix must pass
broader positive/negative, nested, return, async and lifetime regression
coverage before support is claimed.

`benchmark_runtime.py` requires NumPy and optree as well as bearshape/beartype.
It reports versions, origins and repeated timings for strict/Like/Value/context,
nested, tree and diagnostic paths. It also exercises expensive list conversion.
Compare normal installs with matched Python/backend versions on the same idle
host. Results are observations, not a portable performance guarantee or CI
threshold. Keep benchmark outputs outside the tracked package.

## Release evidence

`check_release_evidence.py record` creates a manifest only after archive
integrity checks. `verify` checks the exact source/version/run identity,
canonical filenames and SHA256 bytes, rejecting missing/extra files and
symlinks. The release workflow uses verification immediately before upload and
never rebuilds in the publisher. See the
[release runbook](../docs/maintainers/releasing.md) for commands, approval
prerequisites and recovery. Candidate validation also requires the full native
union probe and integration suite on both Python endpoints; a failure blocks
publication even when baseline CI passes.

## Runtime performance

`tools/benchmark_runtime.py` records raw samples, medians, ranges, versions and
module origins. It covers native controls, strict/Like/Value, nested calls,
plain/composite/Value Trees, multi-axis and variadic shapes, dtype extraction,
casting, diagnostics, decoration and array/Tree validator construction. Compare
normally installed wheels with identical dependencies on the same idle host and
interpreter; do not run validation concurrently. Retain both artifact hashes.
Timings are evidence, not a CI threshold. The
[October audit comparison](evidence/2026-10-11-audit-performance/README.md)
records the corrected baseline and optimized candidate separately from the
unchanged upstream proposal.

The
[remaining optimization comparison](evidence/2026-10-11-remaining-optimization/README.md)
separates dtype and shape preparation, records their combination, and includes
first-use costs, root-only consumers and ordinary beartype overhead.
