---
description: Lightweight root API for dimensions, dtype specs, memo helpers, and factories.
---

# `bearshape`

The root module is intentionally small and optional-dependency-safe. It is the
place to import:

- dimension symbols such as `N`, `C`, `Scalar`, and `Value`
- tree structure symbols such as `T`, `S`, and `Structure`
- `DtypeSpec`
- `make_array_type` and `make_array_like_type`
- `check` and `check_context`
- `__version__`

It does **not** export `Tree` or `make_scalar_like_type`.

## Typical imports

```python
import bearshape
from bearshape import (
  B, C, D, H, K, L, N, P, S, T, W, __,
  Scalar, Dimension, Value, Structure,
  DtypeSpec, make_array_type, make_array_like_type,
  check, check_context,
)
```

## `__version__`

```python
import bearshape

print(bearshape.__version__)
```

In an installed package this is the package version. In a plain source checkout
without installed metadata it falls back to a non-empty string such as
`0+unknown`.

## Pre-defined dimensions

<!-- markdownlint-disable MD013 -->

| Name                                        | Meaning                                  |
| ------------------------------------------- | ---------------------------------------- |
| `N`, `B`, `C`, `D`, `K`, `H`, `W`, `L`, `P` | Named dimensions                         |
| `__`                                        | Anonymous single dimension               |
| `Scalar`                                    | Zero-dimensional array shape             |
| `Value("expr")`                             | Runtime value-based dimension expression |

<!-- markdownlint-enable MD013 -->

Use `Dimension("Name")` to create your own.

## Pre-defined structure symbols

<!-- markdownlint-disable MD013 -->

| Name                | Meaning                      |
| ------------------- | ---------------------------- |
| `T`, `S`            | Named tree structure symbols |
| `Structure("Name")` | Custom tree structure symbol |

<!-- markdownlint-enable MD013 -->

Remember that `Tree` itself lives in `bearshape.optree` or `bearshape.jax`.

## `Dimension`

`Dimension` is a `str` subclass used to build the user-facing shape language.

```python
from bearshape import Dimension

Vocab = Dimension("Vocab")
Embed = Dimension("Embed")
```

Supported operators:

- `~N` for variadic dimensions
- `+N` for broadcastable dimensions
- arithmetic such as `N + 1`, `H * W`, or `2 * C`

`Scalar` cannot participate in arithmetic.

## `Value`

`Value("expr")` is the runtime-value dimension helper.

```python
from bearshape import Value

Batch = Value("batch")
WidthPlus3 = Value("self.width + 3")
```

It supports names, attribute access, numeric literals, and arithmetic. It
rejects calls, indexing, and arbitrary evaluation.

`Value` expressions are trusted developer contracts, not a security sandbox.
Attribute access can execute user-defined properties. Do not construct these
expressions from untrusted input.

## `DtypeSpec`

`DtypeSpec` describes an allowed dtype set and optional byte-order constraint.

```python
from bearshape import DtypeSpec

BF16_OR_F32 = DtypeSpec("BF16orF32", frozenset({"bfloat16", "float32"}))
```

Key features:

- `allowed`: canonical dtype names
- `byteorder`: `"any"`, `"little"`, `"big"`, or `"native"`
- `matches(obj)`: runtime predicate used by array aliases
- `DtypeSpec.structured(dtype)`: exact structured-dtype matcher

## `make_array_type`

`make_array_type(array_type, dtype_spec)` creates a strict array factory for
custom array classes.

```python
import numpy as np
from beartype import beartype
from bearshape import DtypeSpec, N, C, make_array_type

FLOAT32 = DtypeSpec("Float32", frozenset({"float32"}))

MyF32 = make_array_type(np.ndarray, FLOAT32)

@beartype
def f(x: MyF32[N, C]) -> MyF32[N, C]:
  return x
```

The `array_type` needs `.shape` and `.dtype` at runtime. Shape axes must support
Python's integer-index protocol and be nonnegative. Ordinary failures while
reading shape or dtype metadata produce validation failures; cancellation still
propagates. A Like converter owns untrusted input inspection and must return
valid array metadata. Boolean axes retain Python's integer-index meaning
(`False` is zero, `True` is one).

For native static inference from a dynamic factory, use the tested
[complete annotation alias recipe](../features/static-typing.md#custom-factories-and-structured-arrays).

## `make_array_like_type`

`make_array_like_type(dtype_spec, ...)` creates a subscriptable input-contract
factory. Its keyword-only options are `casting="same_kind"`, `name="ArrayLike"`,
`asarray=None` and `trusted_types=None`.

```python
from bearshape import DtypeSpec, make_array_like_type

FLOAT32 = DtypeSpec("Float32", frozenset({"float32"}))

F32Input = make_array_like_type(FLOAT32, name="F32Input")
F32StrictInput = make_array_like_type(FLOAT32, casting="no", name="F32StrictInput")
```

Use backend modules when you want the built-in NumPy/JAX/Torch/CuPy `Like`
aliases. Use the root factory when you want custom dtype combinations or custom
conversion hooks. The `asarray` callable receives the original input and must
return valid `.shape` and `.dtype` metadata; its failure is never retried
through another backend. With no callable, conversion uses NumPy and therefore
requires NumPy at validation time. `trusted_types=()` forces conversion for
every input. An explicit tuple lets those classes bypass conversion. The root
default `trusted_types=None` trusts recognized array classes only when `asarray`
is also `None`; built-in backend factories explicitly trust their native arrays.
The converted value is used only for validation, never substituted for the
function argument.

## `check`

`@bearshape.check` is the explicit memo-management decorator.

```python
import bearshape
from beartype import beartype
from bearshape import N
from bearshape.numpy import F32

@bearshape.check
@beartype
def f(x: F32[N], y: F32[N]) -> F32[N]:
  ...
```

Or combine memo management with `BeartypeConf`:

```python
from beartype import BeartypeConf

@bearshape.check(conf=BeartypeConf())
def f(x: F32[N]) -> F32[N]:
  ...
```

Bare `@check`, `@check()` and `@check(conf=None)` only manage the memo. They
need `@beartype` underneath for type checking. `@check(conf=BeartypeConf())`
applies checking itself. Sync and async functions are supported; generator
functions are rejected. See [memo ownership](../features/decorator.md) and the
[union limitation](../features/composition.md).

## `check_context`

`check_context()` shares one memo across manual `is_bearable()` calls.

```python
from beartype.door import is_bearable
import bearshape
import numpy as np
from bearshape import C, N
from bearshape.numpy import F32

x = np.ones((2, 3), dtype=np.float32)
y = np.ones((2, 3), dtype=np.float32)
with bearshape.check_context():
  assert is_bearable(x, F32[N, C])
  assert is_bearable(y, F32[N, C])
```

It also supports `async with`. Child tasks inherit a live memo by reference;
each task should enter its own context when it needs independent bindings.
