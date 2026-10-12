---
description: Install bearshape with your preferred array backend.
---

<!-- markdownlint-disable-file MD046 -->

# Installation

## Version covered by this guide

This guide describes the **unpublished 0.1.0rc1 development candidate**. As of
12 October 2026, [PyPI provides 0.0.1](https://pypi.org/project/bearshape/),
which has older dependency metadata and behavior. `pip install bearshape` and
`uv add bearshape` select that published release, not this candidate.

The candidate requires **Python >= 3.11** and **beartype >= 0.23.1, < 0.24**.
The maintained matrix is Python **3.11–3.14**, tested with exact beartype
**0.23.1**. Full native composite-union rollback is still a
[release blocker](../features/composition.md); a successful install does not
resolve it.

## Try the candidate with pip

In an activated Python 3.11+ virtual environment, clone the repository and
install the checkout with the baseline dependency and your chosen backend:

```bash
git clone https://github.com/beartype/bearshape.git
cd bearshape
python -m pip install . numpy "beartype==0.23.1"
```

`main` changes over time. For a reproducible experiment, check out the full
reviewed commit SHA before installing. Contributors should instead follow
[the locked development setup](https://github.com/beartype/bearshape/blob/main/CONTRIBUTING.md).

The distribution name and import package are both `bearshape`. There are no
backend extras such as `bearshape[numpy]`; install backend packages explicitly
in the same environment after installing the candidate:

=== "NumPy"

    ```bash
    python -m pip install numpy
    ```

=== "PyTorch"

    ```bash
    python -m pip install numpy torch
    ```

=== "JAX"

    ```bash
    python -m pip install numpy jax
    ```

=== "CuPy"

    Install NumPy and the CuPy distribution matching your CUDA environment. Follow
    [CuPy's installation guide](https://docs.cupy.dev/en/stable/install.html) to
    select the wheel. The plain `cupy` distribution builds from source; do not
    install it alongside a CUDA-specific CuPy wheel.

=== "NumPy + OpTree"

    ```bash
    python -m pip install numpy optree
    ```

    Use `bearshape.optree.Tree`, or install JAX and use `bearshape.jax.Tree`.

!!! note

    `bearshape.jax`, `bearshape.torch`, and `bearshape.cupy` require `numpy`
    alongside the backend. The lightweight root import `import bearshape` does not.
    Choose GPU-enabled JAX/Torch builds using their own installation instructions;
    the repository's development environment deliberately uses CPU packages.

## Try the candidate in a uv project

From your own project, add the source dependency and NumPy:

```bash
uv add "bearshape @ git+https://github.com/beartype/bearshape.git@main" \
  "beartype==0.23.1" numpy
```

Replace `main` with a reviewed full commit SHA to pin an experiment. This is a
consumer setup; development inside bearshape uses `uv sync --locked`.

## Optional dependencies

| Package  | Purpose                                                      |
| -------- | ------------------------------------------------------------ |
| `numpy`  | NumPy array aliases, `ScalarLike`, and backend dtype helpers |
| `torch`  | PyTorch tensor aliases and Torch `Like` types                |
| `jax`    | JAX array aliases, JAX `Like` types, and JAX `Tree`          |
| `cupy`   | CuPy array aliases and CuPy `Like` types                     |
| `optree` | Explicit OpTree backend via `bearshape.optree.Tree`          |

## Import boundaries

The root package is designed to stay optional-dependency-safe:

```python
import bearshape

print(bearshape.__version__)
print(bearshape.N, bearshape.C)
```

That works even in a plain source checkout without installed package metadata.
In that case `__version__` falls back to a non-empty string such as `0+unknown`.

Backend modules are stricter:

- `bearshape.numpy` needs `numpy`
- `bearshape.jax` needs `jax` and `numpy`
- `bearshape.torch` needs `torch` and `numpy`
- `bearshape.cupy` needs `cupy` and `numpy`
- `bearshape.optree` needs `optree`

## Verify installation

```python
import bearshape
print(bearshape.__version__)
```

Then verify the backend you actually plan to use:

```python
from bearshape import N, C
from bearshape.numpy import F32
```

## Release readiness

The [composition guide](../features/composition.md) explains the known union
defect. The [release runbook](../maintainers/releasing.md) records supported
upstream adoption, exact-artifact validation and publishing prerequisites. The
candidate is independently versioned from beartype; it has not been published
merely because its implementation PRs are merged.
