# bearshape

[![Python 3.11-3.14](https://raw.githubusercontent.com/beartype/bearshape/main/docs/assets/images/python_versions_badge.svg)](https://www.python.org/)
[![Docs](https://img.shields.io/badge/docs-live-526CFE?style=flat-square&logo=readthedocs&logoColor=white&labelColor=1F2937)](https://beartype.github.io/bearshape/)

Runtime shape and dtype checking for NumPy, JAX, PyTorch, CuPy, and
tree-structured containers, powered by
[beartype](https://github.com/beartype/beartype).

```python
from beartype import beartype
from bearshape import N, C
from bearshape.numpy import F32


@beartype
def normalize(x: F32[N, C]) -> F32[N, C]:
  return x / x.sum(axis=1, keepdims=True)
```

bearshape turns annotations such as `F32[N, C]`, `F32Like[~B, C]`,
`F32[Value("size")]`, and `Tree[F32[N], T]` into runtime-validated contracts.
Named dimensions are shared within a function call, so mismatched shapes fail at
the boundary instead of later in array code.

## Installation and candidate status

These docs describe the **unpublished 0.1.0rc1 candidate**, requiring Python
**3.11+** (tested on 3.11–3.14) and beartype **0.23.1**. `pip install bearshape`
currently installs the older
[PyPI release](https://pypi.org/project/bearshape/). To try the candidate from a
checkout in a Python 3.11+ virtual environment:

```bash
python -m pip install . numpy "beartype==0.23.1"
```

Install your backend explicitly; the root import loads none. See the
[installation guide](https://github.com/beartype/bearshape/blob/main/docs/getting-started/installation.md)
for checkout, uv, JAX, Torch, CuPy and OpTree instructions.

**Release is blocked by native composite-union rollback in beartype 0.23.1.** A
failed union alternative can leave dimension bindings that reject a later valid
alternative. `check` and `check_context` do not fix that boundary. See
[composition and limitations](https://github.com/beartype/bearshape/blob/main/docs/features/composition.md)
for a reproducer and the distinction between normal checks and the unshipped
upstream proposal.

## What It Checks

- strict array type, dtype, and shape contracts
- backend-aware `Like[...]` conversion checks
- scalar-like values and constrained runtime `Value(...)` dimensions
- tree leaf and structure annotations through JAX or OpTree
- annotation syntax exercised by pyright, mypy, ty, and pyrefly consumer
    fixtures

## Public Surface

Import dimensions, `Value`, `Scalar`, `DtypeSpec`, `check`, and `check_context`
from `bearshape`.

Import backend aliases from backend modules:

```python
from bearshape.numpy import F32, F32Like
from bearshape.jax import Tree
from bearshape.torch import I64
```

The root package does not import NumPy or any backend. Backend modules require
their own runtime dependencies.

## Development

```bash
uv sync --locked
uv run --locked prek install
uv run --locked prek run -a
uv run --locked pytest tests/ --ignore=tests/test_typecheck.py -n auto
uv run --locked pytest tests/test_typecheck.py -q
```

Use uv 0.13.0. See
[CONTRIBUTING.md](https://github.com/beartype/bearshape/blob/main/CONTRIBUTING.md)
for setup, focused PRs, regression expectations, review and artifact validation.
CuPy runtime tests require CUDA hardware. The
[static typing guide](https://github.com/beartype/bearshape/blob/main/docs/features/static-typing.md)
distinguishes checker-supported annotations from runtime-only shape expressions.
