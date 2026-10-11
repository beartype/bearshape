---
description: Package-wide instrumentation with beartype.claw — no per-function decorators.
---

<!-- markdownlint-disable-file MD046 -->

# Import Hook (beartype.claw)

If you want package-wide instrumentation rather than decorating individual
functions, use `beartype.claw` or bearshape's alias for its package hook.

## Usage

=== "Via bearshape"

    ```python
    from bearshape.claw import bearshape_this_package
    bearshape_this_package()
    ```

=== "Via beartype directly"

    ```python
    from beartype.claw import beartype_this_package
    beartype_this_package()
    ```

`bearshape_this_package()` is a direct alias for
`beartype.claw.beartype_this_package()`. Runtime behavior is the same.

## What it gives you

Once called in `your_package.__init__`, all subsequently imported submodules in
that package are instrumented as if their annotated callables had been decorated
with `@beartype`.

```python
# your_package/__init__.py
from bearshape.claw import bearshape_this_package
bearshape_this_package()

# your_package/model.py
from bearshape import N, C
from bearshape.numpy import F32

def forward(x: F32[N, C]) -> F32[N, C]:
  ...
```

Because bearshape integrates through standard beartype validators, the usual
cross-argument dimension semantics still apply.

## Configuration

Pass a `BeartypeConf` to customize the checking behavior:

```python
from beartype import BeartypeConf
from bearshape.claw import bearshape_this_package

bearshape_this_package(conf=BeartypeConf(
  is_color=False,
))
```

## When to use

<!-- markdownlint-disable MD013 -->

| Approach                                   | Best for                                 |
| ------------------------------------------ | ---------------------------------------- |
| `@beartype` per function                   | Fine-grained control, specific functions |
| `beartype.claw` / `bearshape_this_package` | Entire packages, library-wide checking   |

<!-- markdownlint-enable MD013 -->

## Diagnosing competing import hooks

Another import hook can take precedence and prevent package instrumentation.
After installing your application's hooks, call beartype's public diagnostic
during single-threaded startup:

```python
from beartype.claw import warn_if_beartype_claw_inactive

warn_if_beartype_claw_inactive()
```

It warns when beartype's hook is inactive; it does not repair the competing hook
or retroactively check imported functions. Keep `bearshape_this_package()` in
your package initializer: it is a caller-sensitive direct alias.
