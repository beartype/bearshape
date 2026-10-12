# Contributing

The current development candidate is **0.1.0rc1**, with Python **3.11–3.14** and
exact **beartype 0.23.1** in validation. It is unpublished. Normal CI is green,
but the [native-union release blocker](docs/features/composition.md) remains
open. Local upstream patches are proposal evidence, not a supported replacement
dependency.

## From an idea to a reviewed change

1. For a bug, describe the smallest reproducer, expected/actual behavior and
    Python, bearshape, beartype and backend versions in an issue or draft PR.
    For a public-contract change, agree on scope before implementing it. Keep
    independent fixes and optimizations in separate PRs.
1. Fork the repository if you do not have write access, then clone your fork.
    Add `https://github.com/beartype/bearshape.git` as an `upstream` remote.
    Contributors with write access can clone that repository directly. Work
    from current `main` in a feature branch; do not edit or force-push main.
1. For features, contract changes, CI/release work, substantial docs or
    refactors, create a dedicated worktree, commit an ExecPlan under `plans/`
    following [PLANS.md](PLANS.md), then open a draft PR before implementation.
    Small, low-risk corrections can use a normal feature branch. State
    dependencies when stacking PRs. [The plan index](plans/README.md) separates
    active guidance from dated implementation records.
1. Reproduce a bug with a failing regression where practical, then make the
    smallest fix. Preserve annotation syntax, useful errors and backend import
    boundaries. Use the existing two-space Python indentation. Changes to state
    ownership need failure, nesting, async and lifetime evidence; typing
    changes need positive, negative and native inference consumers in all four
    engines.
1. Run the relevant local checks below and update affected guides/examples and
    the changelog for user-visible changes. Keep the ExecPlan's progress,
    decisions and results current. Distinguish local results, hosted checks,
    expected skips and known release blockers. Never hide a defect with an
    xfail, a removed negative fixture or a lower coverage threshold.
1. Push to your branch or fork and target `beartype/bearshape:main`. The PR
    should explain the user-visible problem and behavior, link its plan/issue,
    list dependencies and give the commands/results needed to review it. Mark
    it ready when implementation and required checks pass; address review
    feedback in focused commits.
1. Maintainers merge only with explicit approval and successful checks on the
    reviewed history. Preserve all reviewed heads and integration resolutions,
    verify main, then remove only clean merged branches/worktrees after saving
    useful evidence. Merge approval never authorizes publication, deployment,
    access changes or upstream messages.

A worktree is a second checkout sharing the same Git history. From a clean,
up-to-date local main, a substantial change can start with:

```bash
git worktree add ../bearshape-my-change -b my-change main
cd ../bearshape-my-change
```

Run the setup below inside that checkout. Push to your fork's remote when using
one; you do not need release credentials, organization access or CUDA hardware
to contribute CPU changes. Report an unavailable hardware check explicitly.

## Local Development

Install Git and uv, and select a supported Python interpreter. The repository
uses uv-managed Python and uv can download a missing interpreter during sync.
For example, `uv sync --locked --python 3.11` selects the oldest supported
version; use `--python 3.14` in a separate environment for endpoint validation.

The canonical repository is
[beartype/bearshape](https://github.com/beartype/bearshape). Only for an old
checkout whose `origin` still points to the former canonical owner (not a fork),
update that URL:

```bash
git remote set-url origin https://github.com/beartype/bearshape.git
```

Use **uv 0.11.17** (the project accepts uv 0.11.x). To bootstrap it alongside a
different global uv version, run `uv tool install uv==0.11.17` from outside this
checkout, then ensure its executable is first on PATH.

```bash
uv sync --locked
uv run --locked prek install
uv run --locked prek run -a
uv run --locked pytest tests/ --ignore=tests/test_typecheck.py -n auto
uv run --locked pytest tests/test_typecheck.py -q
```

When upgrading an existing checkout from the earlier hook configuration, remove
its unused commit-message shim once with
`uv run --locked prek uninstall --hook-type commit-msg`, then run the install
command above. File checks default to pre-commit. Runtime/checker checks remain
at pre-push, environment sync at checkout/merge/rewrite, and actionlint manual.
CI verifies installation and that commit-message paths do not enter file checks.

The checker harness runs pyright, mypy, ty and pyrefly against source and real
positive/negative/inference consumers, with interpreter-matched settings. Direct
checker commands are useful for debugging but do not replace that harness. Use
`-n auto` for runtime tests; use `-n0` for narrow serial debugging.

The default groups include CPU NumPy/JAX/Torch/optree, all four checkers, tests,
docs, notebook and development tools. Use exact
`uv sync --locked --only-group <group>` or a fresh venv when proving dependency
isolation: `uv run --only-group` can retain packages from earlier runs. CuPy
runtime validation needs real CUDA hardware. The
[handoff report](docs/maintainers/production-readiness.md) records GPU evidence
and the accepted limits of native CuPy static typing.

Agent instructions are shared by `AGENTS.md` and the `CLAUDE.md` symlink.
`PLANS.md` describes major-work plans; [tools/README.md](tools/README.md)
describes the validation scripts, their inputs and what their results prove.

## Repository map and choosing checks

`src/bearshape/` contains the lightweight root API, shared validators and
explicit backend modules. Runtime regressions live in `tests/test_*.py`;
positive/static inference consumers live in `tests/typing/`, with deliberately
invalid callers in `tests/typing_negative/`. `docs/` is the website, and
`examples/bearshape_tour.ipynb` is its executable tour. `tools/` contains
existing validators; `.github/workflows/validate.yml` is the shared acceptance
matrix. Plans and `tools/evidence/` retain dated experiments, not current
install recipes.

<!-- markdownlint-disable MD013 -->

| Changed surface                    | Relevant checks in addition to normal hooks                                  |
| ---------------------------------- | ---------------------------------------------------------------------------- |
| Runtime / backend / memo           | Runtime suite above; affected backend/floor and lifetime cases               |
| Static aliases / public signatures | Full `tests/test_typecheck.py` consumer harness                              |
| User docs / examples               | Docs build and rendered/syntax check; execute affected examples and notebook |
| Dependencies / package metadata    | Locked sync, relevant tox factors, archive integrity and installed consumers |
| Workflow / release tooling         | Manual actionlint, relevant tooling regressions and actual hook stages       |

<!-- markdownlint-enable MD013 -->

Normal hooks run on every change; the actual pre-push hook runs runtime and
four-checker validation. The docs checker parses snippets but does not execute
them. Exercise changed runnable examples as real calls, including their intended
failures; compilation alone is insufficient. The full hosted matrix remains
required even when only a smaller local check is relevant.

For a fresh minimal consumer, build the archives first, then use a new venv:

```bash
uv venv build/minimal --python 3.11
uv pip install --python build/minimal/bin/python \
  dist/bearshape-0.1.0rc1-py3-none-any.whl "beartype==0.23.1"
build/minimal/bin/python -I tools/smoke_minimal.py
```

On Windows use `build\minimal\Scripts\python.exe`. Substitute the current
project version and repeat with Python 3.14 when that boundary changes. Do not
reuse a populated development environment to prove optional-dependency
isolation.

## Tox environments and CI

Runtime factors use `{python}-{beartype}-{backend}`; checker factors use
`{python}-{beartype}-type-{checker}`. For example:

```bash
uv run --locked tox list
uv run --locked tox run -e py311-bt0231-cpu
uv run --locked tox run -e py314-bt0231-cpu
uv run --locked tox run -e py311-bt0231-numpy22
uv run --locked tox run -e py313-bt0231-type-pyright1408
uv run --locked tox run -e py313-bt0231-type-mypy119
uv run --locked tox run -e py313-bt0231-type-ty
uv run --locked tox run -e py313-bt0231-type-pyrefly
```

Type environments install all CPU backends. CuPy is not part of those lanes.
`dev` uses the current lock; explicit backend/checker factors exercise the
configured compatibility ranges. Every baseline lane requires exact beartype
0.23.1. Native composite-union rollback remains a release blocker and requires a
supported upstream integration; passing these lanes alone does not close it.

Pull requests, main pushes, nightly and candidate validation use the same
required matrix in `.github/workflows/validate.yml`. When adding a version,
update `tox.toml`, `tools/validate_tox_env.py`, the runtime preflight, lockfile
and shared workflow as applicable. The dependency range alone does not prove
compatibility with a new version.

## Check release archives

Build the source distribution first, then build the wheel from that archive:

```bash
uv build --sdist
uv build dist/bearshape-<version>.tar.gz --wheel
uv run --locked --only-group dev python tools/check_distribution.py \
  dist/bearshape-<version>-py3-none-any.whl dist/bearshape-<version>.tar.gz
```

Replace `<version>` with the project version. The check verifies license text,
metadata, inline typing information, matching package contents, and downstream
test inputs. It prints artifact hashes for release evidence. The source archive
includes the tests, lockfile and configuration needed to run `uv sync --locked`
and `uv run --locked pytest`. For the complete contributor workflow, use a Git
checkout: the archive does not include the website sources, plans or GitHub
configuration. CuPy still requires a separate CUDA environment.

## Candidate validation

CI and nightly use `.github/workflows/validate.yml`. Current locked CPU backends
run on Python 3.11–3.14 on Linux, with endpoint jobs on macOS and Windows.
Four-checker consumer tests run on every supported Python on Linux. Separate tox
jobs exercise backend and checker floors with exact beartype 0.23.1.
`tools/validate_runtime.py` fails if an expected backend is absent or Torch is a
CUDA/ROCm build in a CPU lane. Optional local skips do not establish support.

Use `uv run --locked prek run -a` for the normal hooks and
`uv run --locked prek run actionlint -a --stage manual` for workflow checks.
Pre-push checks use the locked four-checker harness and runtime suite. The
required CI gate accepts only successful completion of every required job. CuPy
GPU validation remains a separate hardware-backed requirement.

To validate the installed artifact after building the sdist and its wheel, run:

```bash
uv run --locked python tools/check_installed.py \
  dist/*.whl dist/*.tar.gz --python 3.11
```

Repeat with `--python 3.14`. The command installs locked dependencies and the
wheel normally in a temporary environment, then runs copied runtime and checker
fixtures with no package source directory. It reports artifact hashes and
installed module origins. `--installed-package` is an explicit pytest mode for
this consumer check; ordinary source validation continues to include `src`.

The separate read-only `upstream-proposal.yml` workflow applies the reviewed
patch series only in disposable upstream checkouts and validates installed
consumers at both Python endpoints.
[Its reproduction guide](tools/upstream/README.md) is for work on the open
integration boundary. Do not apply those patches to a normal development
environment or treat its green result as published support.

## Validate and publish a release

The [maintainer release runbook](docs/maintainers/releasing.md) describes
preparation, exact-artifact review, external prerequisites, future publication
and failure recovery. Full native-union composition is an additional required
release gate; published beartype 0.23.1 currently fails it.

Run a validation-only workflow before making a release decision:

```bash
gh workflow run pypi.yml --repo beartype/bearshape --ref main \
  -f ref=<reviewed-commit> -F publish=false
```

This resolves one commit, runs the complete shared matrix, and produces
`candidate-distributions` plus `release-evidence`. The evidence records the
source SHA, version, artifact hashes and run URL. A failed required check
prevents publication. GPU runtime evidence and open contract decisions still
require review; CPU CI does not replace them.

Publication requires a canonical `v<project-version>` tag already in `main`
history. Both the workflow and package must come from that exact tag and commit.
Versions use `X.Y.Z` with an optional `aN`, `bN` or `rcN` suffix. A GitHub
release must be marked as a prerelease exactly when its version has such a
suffix. After explicit owner approval, publish that GitHub release, or dispatch
the workflow from the same tag with `publish=true`. Publishing downloads the
same tested distributions and does not rebuild them. Only that job receives OIDC
permission and enters the `pypi` environment.

Before enabling publication, configure required review for `pypi`, prevent
self-approval and administrator bypass, and limit its deployment policy to
release tags. Protect `main` and release tags, and require the final validation
check on pull requests. Confirm the PyPI trusted publisher identifies the actual
repository owner/name, `pypi.yml`, and environment `pypi`. The workflow does not
create these controls. The 2026-09-08 inspection found unprotected `main`, no
repository rulesets and no `pypi` approval reviewers; PyPI configuration remains
unverified. The GitHub transfer to `beartype/bearshape` was verified on
2026-09-10.

Before the next release, a PyPI project owner must inspect
[the publishing settings](https://pypi.org/manage/project/bearshape/settings/publishing/)
and ensure the trusted publisher has repository owner `beartype`, repository
name `bearshape`, workflow filename `pypi.yml`, and environment `pypi`. GitHub
repository redirects do not update that external trust configuration. See
[PyPI's publisher setup](https://docs.pypi.org/trusted-publishers/adding-a-publisher/).
Keep OIDC; do not add an upload token. GitHub transfer does not establish PyPI
ownership. Published version `0.0.1` still carries its original URL metadata;
these repository edits update future distributions, not already published files.

## Documentation validation and deployment

```bash
uv run --locked --only-group docs zensical build --clean
uv run --locked --only-group docs python tools/check_docs.py
uv run --locked python tools/check_notebook.py
```

CI validates rendered structures, Python snippet syntax and notebook execution.
Main/docs pushes build Pages artifacts but do not deploy them. After explicit
deployment approval, dispatch `docs.yml` from the reviewed `main` or `docs`
branch. Only its deployment job receives Pages/OIDC write permissions and enters
the `github-pages` environment. Merging code does not authorize deployment.

The production site is <https://beartype.github.io/bearshape/>. After approval:

```bash
gh workflow run docs.yml --repo beartype/bearshape --ref main
```

Pages must use GitHub Actions as its build source, with `main` allowed by the
`github-pages` environment. These settings and a successful deployment were
verified after the transfer on 2026-09-10. Check the resulting workflow and open
the home page, a nested guide, and the logo after deployment. GitHub redirects
old repository links, but
[does not redirect transferred Pages sites](https://docs.github.com/en/repositories/creating-and-managing-repositories/transferring-a-repository).
Use the new website address for saved links. Do not recreate the old repository
to add a redirect, because that would replace GitHub's repository redirect.

## Dependency canary and custom annotations

Nightly keeps the locked validation matrix and adds a separate latest-compatible
runtime/backend canary on Python 3.11 and 3.14. Its temporary lock and version
artifacts explain failures before any dependency update is proposed. The
canary's range-based preflight is not release acceptance; normal CI and releases
keep exact beartype 0.23.1 until supported upstream integration is adopted.

Dynamic custom/Structured factory examples must include real positive, negative
and native inference consumers in the four-checker harness. Use the tested
[complete native alias recipe](docs/features/static-typing.md#custom-factories-and-structured-arrays)
and execute its runtime branch as well. Constructor/repr checks and inferred
`Any` are not evidence of native consumer support.
