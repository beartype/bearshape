# Validating and publishing bearshape

Publication is a separate owner decision after candidate validation. Merging a
PR does not authorize a PyPI upload or a Pages deployment. Use the
validation-only route below while preparing the next release.

## Current release blocker

Released beartype 0.23.1 does not roll back a failed native composite-union
alternative's bearshape bindings. The original probe and expanded integration
suite are mandatory release gates on Python 3.11 and 3.14. They currently fail
with the published dependency. A tested local upstream proposal is useful
engineering evidence, but cannot substitute for an available supported release.
Do not skip, mark xfail, or remove these gates to publish.

Ordinary CI and nightly validate the selected Python/dependency baseline and all
ordinary regression cases. Release validation additionally requires the complete
composition contract from the normally installed candidate wheel. The gate
collects `tools/upstream/` as a directory so union, scope, isolation and audit
composition modules all run. Tests from the optional patched upstream source are
not substituted for this published-dependency gate. Once supported upstream
integration is adopted, promote the transaction cases into the normal source and
installed-archive suites as well.

## Prerequisites owned by maintainers

Before any upload, verify the following settings with the repository and PyPI
owners. Workflow files do not configure these controls:

- Protect `main` with pull-request review and the actual **Required validation**
    check from the reusable CI workflow. Require checks on the reviewed head;
    prohibit force pushes and deletion.
- Protect release tags matching `v*` against update/deletion and restrict their
    creation to authorized release maintainers. Do not move a published tag.
- Configure the `pypi` environment with required reviewers, prevent
    self-approval, disable administrator bypass, and allow only approved version
    tags. Remove its old `main` branch deployment exception.
- A PyPI project owner must verify ownership/recovery access and the trusted
    publisher: owner **beartype**, repository **bearshape**, workflow
    **pypi.yml**, environment **pypi**. Inspect the private publishing settings
    directly. GitHub ownership transfer does not update or prove this external
    trust.
- Obtain fresh CUDA/CuPy results for the exact candidate wheel, including source
    SHA, wheel hash, interpreter/backend/driver versions and actual device. CPU
    skips and older GPU logs do not validate a changed candidate.

The October 2026 audit found the GitHub protections/reviewers incomplete and
PyPI trust unverified. Keep them outstanding until there is actual verification.

The project can remain owned by a personal PyPI account. Its owner configures
**Publishing → Trusted Publisher**, separately from the **Collaboration** page
that manages project roles. No PyPI organization transfer is required. The
GitHub `pypi` environment reviewer is a separate approval: preventing
self-approval requires someone other than the person starting the release.
Choose that reviewer before enabling publication; keep the choice pending while
preparing the candidate.

## Dependency canary

Nightly also runs a separate latest-compatible dependency canary at both Python
endpoints. It upgrades beartype, NumPy, JAX/jaxlib, Torch, optree and
`typing-extensions` within the declared constraints in a disposable lock, keeps
the maintained checker toolchain and records the resolved inputs. Failures are
visible and must be investigated before proposing a lock update. The canary uses
`validate_runtime.py cpu --latest-compatible`; normal/release acceptance keeps
the exact preflight. A passing canary neither repairs the known union blocker
nor authorizes publishing.

## Prepare a candidate

Use uv 0.13.0 and Python 3.11–3.14. If a global uv version is outside the
project's 0.13 range, bootstrap `uv tool install uv==0.13.0` outside the
checkout and put that executable first on PATH. From the repository root:

```bash
uv sync --locked
uv run --locked prek install
uv run --locked pytest tests/ --ignore=tests/test_typecheck.py -n auto
uv run --locked pytest tests/test_typecheck.py -q
uv run --locked prek run -a
uv run --locked prek run actionlint -a --stage manual
```

Update the independently versioned bearshape version in `pyproject.toml`,
refresh `uv.lock`, and write the changelog and migration notes in a reviewed PR.
Refresh candidate/release notices in README, installation, the tour and the
current handoff at the same time; existing PyPI metadata and the deployed site
do not change when source docs are merged. Versions must be canonical `X.Y.Z`,
optionally followed by `aN`, `bN` or `rcN`. Do not change the version just to
match beartype. Keep exact dependency preflights, tox, CI and the lock
synchronized when adopting an upstream release.

Build into an empty output directory: a candidate consists of exactly one source
archive and one pure-Python wheel. Build the wheel from the source archive, then
check both archives and normal consumers:

```bash
uv build --sdist
uv build dist/bearshape-<version>.tar.gz --wheel
uv run --locked python tools/check_distribution.py dist/*.whl dist/*.tar.gz
uv run --locked python tools/check_installed.py \
  dist/*.whl dist/*.tar.gz --python 3.11
uv run --locked python tools/check_installed.py \
  dist/*.whl dist/*.tar.gz --python 3.14
```

Replace `<version>` with the candidate version. Preserve old evidence in a
separate directory instead of mixing versions in `dist/`. The source archive
includes consumer tests; the installed check runs them without the package
source folder. Minimal consumers must use fresh environments with no optional
backend. The shared hosted matrix also checks platform endpoints, all four
static engines, backend/checker floors, coverage, rendered docs and notebook
execution.

### Final CUDA evidence

Use an owner-approved CUDA environment with a fresh virtual environment and a
CuPy distribution compatible with its driver. Install the exact reviewed wheel
normally, plus the copied source archive's test dependencies; do not install the
bearshape checkout in editable mode. Record `pip freeze` (or `uv pip list`),
source SHA and the wheel's SHA256, then run the environment's interpreter:

```bash
python -I -c "import cupy; assert cupy.cuda.runtime.getDeviceCount() > 0; cupy.show_config()"
python -I -c "import bearshape, pathlib, sys; assert pathlib.Path(bearshape.__file__).resolve().is_relative_to(pathlib.Path(sys.prefix).resolve())"
python -I -m pytest <copied-consumer>/tests/test_cupy.py \
  --installed-package -n 0
```

Repeat at both supported endpoint interpreters, retain device/driver details and
complete test results, and investigate any skip. CPU-only skips, prior wheels
and historical GPU reports cannot substitute for this evidence.

## Run validation without publishing

Dispatch the release workflow from the reviewed branch/tag containing the
pipeline, with an explicit source commit and publication disabled:

```bash
gh workflow run pypi.yml --repo beartype/bearshape \
  --ref <reviewed-branch-or-tag> \
  -f ref=<reviewed-commit> -F publish=false
```

Use the full 40-character commit SHA for `<reviewed-commit>`; checkout does not
resolve an abbreviated SHA reliably. A branch or tag is appropriate for `--ref`,
which selects the workflow definition.

The workflow resolves the source once. Shared validation builds and tests
`candidate-distributions`; the additional composition jobs install that wheel
normally and exercise the union contract. Only successful required validation
and composition checks produce `release-evidence`. A blocked union is a failed
release validation, never a successful dry run. The publishing job is skipped
when `publish=false`.

Review the workflow's source SHA and job results, then download both artifacts:

```bash
gh run download <run-id> --repo beartype/bearshape \
  -n candidate-distributions -D candidate/dist
gh run download <run-id> --repo beartype/bearshape \
  -n release-evidence -D candidate/evidence
python tools/check_release_evidence.py verify \
  candidate/evidence/release-evidence.json candidate/dist \
  --source-sha <reviewed-commit> --version <version> \
  --run-url https://github.com/beartype/bearshape/actions/runs/<run-id>
```

The manifest binds the version, source, originating run, canonical filenames and
SHA256 hashes. Verification rejects additional files, missing archives,
symlinks, changed bytes or substituted identity. Retain the manifest, full test
results and matching GPU evidence in the release review packet.

## Publish later, after explicit approval

This section documents a future authorized action. No publication is part of the
October implementation task. After review, merge the approved source and verify
its final main checks. Create the canonical `v<version>` tag on that exact
commit; it must already belong to `origin/main` history. The publishing workflow
itself must execute from the same tag and commit.

Choose one trigger: publish the corresponding GitHub release, marking it as a
prerelease exactly when the version has an a/b/rc suffix, **or** explicitly
dispatch from the tag:

```bash
gh workflow run pypi.yml --repo beartype/bearshape --ref v<version> \
  -f ref=v<version> -F publish=true
```

Every publishing run performs full validation. Before approving its `pypi`
environment, review that run's evidence and exact hashes; a previous dry run is
not an approval of different bytes. The upload job downloads those same
artifacts, verifies their manifest again and uses OIDC trusted publishing. It
never rebuilds the package and receives no long-lived upload token. Concurrent
attempts for the same tag are serialized without cancelling an in-progress
publication.

After success, verify the PyPI version, metadata and downloadable archive hashes
against the manifest, then test a fresh normal install from PyPI. Update release
notes and close the release-request issue only after the release exists. Pages
has its own manually approved deployment procedure in CONTRIBUTING.

## Failure and recovery

If any validation or evidence check fails, repair it in a reviewed source change
and run validation again. Do not bypass the failure or replace artifact bytes in
an existing evidence packet. A missing GitHub artifact requires a new complete
validation run, not a local rebuild uploaded without its checks.

If upload fails, inspect PyPI before retrying. PyPI versions/files are
immutable; never move the tag, overwrite a released version, or enable
skip-existing to hide a partial publication. If nothing was uploaded, retry only
with the same validated artifacts and reviewed identity. If publication was
partial or wrong, coordinate a new version with the PyPI owner and document what
happened. No token fallback is part of the process: fix the trusted-publisher
identity or environment approval instead.
