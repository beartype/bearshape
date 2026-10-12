---
description: Current native-union limitation, container sampling, and release status.
---

# Composition and limitations

The unpublished 0.1.0rc1 candidate is validated with released beartype 0.23.1.
Ordinary array, dtype, dimension, Like and Tree tests pass. Full composition
through native union alternatives still has a known correctness defect, so
release readiness remains withheld.

## A failed union alternative can leave bindings behind

Consider this valid call:

```python
import numpy as np
from beartype import beartype
from bearshape import C, N
from bearshape.numpy import F32

@beartype
def choose(pair: tuple[F32[N], str] | tuple[F32[C], int], y: F32[N]) -> None:
  pass

choose((np.ones(2, dtype=np.float32), 1), np.ones(3, dtype=np.float32))
```

The first alternative binds `N=2`, then fails because `1` is not a string. The
second succeeds with `C=2`. The last argument should independently bind `N=3`,
but the failed alternative's binding survives in beartype 0.23.1 and the call is
rejected. The same missing rollback boundary can affect more complex containers,
aliases and tree constraints. A failed individual array check can restore its
own changes; it cannot see a later failure of its enclosing branch.

Explicit `@check` and `check_context()` manage memo lifetime; they do not repair
this union boundary. Passing ordinary CI does not establish full composition.
The standalone reproducer is `tools/probe_union.py`; its nonzero exit with the
published baseline is evidence of this open defect, not an expected passing run.

The repository contains a tested
[upstream proposal](https://github.com/beartype/bearshape/blob/main/tools/upstream/README.md)
for invocation scopes and transaction rollback. It is not installed or applied
by bearshape and has not shipped in the supported dependency. Its local test
results do not make the published dependency correct. Supported upstream
integration and the full release matrix are required before this blocker closes.

## Containers and checking frequency

For native containers such as `list[F32[N]]`, beartype decides which items to
inspect according to its configuration. `BeartypeConf(is_random=False)` makes
sampling deterministic by selecting the first item; it does not check all items.
In contrast, bearshape's `Tree[F32[N]]` visits every leaf recognized by the
selected JAX or OpTree registry and shares dimensions across those leaves.

Runtime checks occur at Python wrapper boundaries. JAX tracing and Torch
compilation can change their frequency; see
[framework transformations](frameworks.md). Like validation may convert a
temporary value, but the function receives its original argument and must
convert it explicitly before using native methods.

## Runtime and static guarantees

Static checkers preserve the supported native array interfaces and input
families; they do not prove dimension values, shape arithmetic or tree
registration. See [static typing](static-typing.md), including the limited CuPy
protocol. Runtime CUDA evidence is separate from CPU and static checks.

The [release runbook](../maintainers/releasing.md) owns the remaining release
prerequisites. Neither a merged PR nor a successful proposal test authorizes
publishing a package.
