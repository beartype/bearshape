"""Measure representative runtime costs without imposing a timing gate."""

from __future__ import annotations

import argparse
import json
import platform
import statistics
import sys
import timeit
from collections.abc import Callable
from functools import partial
from importlib.metadata import version
from typing import Annotated

import numpy as np
from beartype import BeartypeConf, beartype
from beartype.roar import BeartypeCallHintParamViolation
from beartype.vale import Is

import bearshape
from bearshape import C, N, Value, check
from bearshape._array_types import _ArrayChecker
from bearshape._dtypes import FLOAT32, extract_dtype_str
from bearshape._shape import NamedDim
from bearshape._tree import _TreeChecker
from bearshape.numpy import F32, F32Like
from bearshape.optree import Tree, _get_optree


def bare(value: np.ndarray) -> np.ndarray:
  return value


@beartype
def native(value: np.ndarray) -> np.ndarray:
  return value


@beartype
def strict(value: F32[N]) -> F32[N]:
  return value


@check(conf=BeartypeConf())
def explicit(value: F32[N]) -> F32[N]:
  return value


@beartype
def like(value: F32Like[N]) -> object:
  return value


@check(conf=BeartypeConf())
def value_dimension(size: int, value: F32[Value("size")]) -> F32[Value("size")]:  # ruff: ignore[unused-function-argument]
  """The size argument is consumed by the Value annotations."""
  return value


@check(conf=BeartypeConf())
def nested(value: F32[N]) -> F32[N]:
  return strict(value)


@beartype
def tree(value: Tree[F32[N]]) -> Tree[F32[N]]:
  return value


@beartype
def tree_value(size: int, value: Tree[F32[Value("size")]]) -> Tree[F32[Value("size")]]:  # ruff: ignore[unused-function-argument]
  return value


@beartype
def tree_composite(value: Tree[Annotated[F32[N], Is[lambda _value: True]]]) -> object:
  return value


@beartype
def multiaxis(value: F32[N, 3, C, N + 1]) -> F32[N, 3, C, N + 1]:
  return value


@beartype
def variadic(value: F32[N, ~C, N + 1]) -> F32[N, ~C, N + 1]:
  return value


def construct_array_validator() -> object:
  return _ArrayChecker(np.ndarray, FLOAT32, (NamedDim("N"),))


def decorate_array() -> object:
  def consume(value: F32[N]) -> F32[N]:
    return value

  return beartype(consume)


def construct_tree_validator() -> object:
  return _TreeChecker(F32[N], get_ops=_get_optree)


def diagnostic(value: np.ndarray) -> None:
  try:
    strict(value)
  except BeartypeCallHintParamViolation:
    return
  message = "Benchmark's invalid input unexpectedly passed"
  raise AssertionError(message)


def measure(
  label: str, call: Callable[[], object], *, calls: int, repeats: int
) -> dict[str, str | int | float | list[float]]:
  call()
  samples = [
    seconds * 1_000_000 / calls
    for seconds in timeit.repeat(call, number=calls, repeat=repeats)
  ]
  return {
    "case": label,
    "calls_per_repeat": calls,
    "repeats": repeats,
    "samples_us": samples,
    "median_us": statistics.median(samples),
    "min_us": min(samples),
    "max_us": max(samples),
  }


def main() -> None:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("--calls", type=int, default=10_000)
  parser.add_argument("--repeats", type=int, default=5)
  args = parser.parse_args()
  if args.calls < 1 or args.repeats < 1:
    parser.error("calls and repeats must be positive")
  results = []
  for size in (3, 1_000_000):
    array = np.ones(size, dtype=np.float32)
    results.extend(
      measure(
        f"{function.__name__}/{size}",
        partial(function, array),
        calls=args.calls,
        repeats=args.repeats,
      )
      for function in (bare, native, strict, explicit, like, nested)
    )
    results.append(
      measure(
        f"value/{size}",
        partial(value_dimension, size, array),
        calls=args.calls,
        repeats=args.repeats,
      )
    )
    sequence = array.tolist()
    results.append(
      measure(
        f"like-sequence/{size}",
        partial(like, sequence),
        calls=min(args.calls, max(5, 5_000_000 // size)),
        repeats=args.repeats,
      )
    )
    invalid = np.ones(size, dtype=np.int32)
    results.append(
      measure(
        f"diagnostic/{size}",
        partial(diagnostic, invalid),
        calls=min(args.calls, 1_000),
        repeats=args.repeats,
      )
    )
  for leaves in (1, 100):
    arrays = [np.ones(3, dtype=np.float32) for _ in range(leaves)]
    results.append(
      measure(
        f"tree/{leaves}",
        partial(tree, arrays),
        calls=max(1, args.calls // leaves),
        repeats=args.repeats,
      )
    )
    for label, call in (
      ("tree-value", partial(tree_value, 3, arrays)),
      ("tree-composite", partial(tree_composite, arrays)),
    ):
      results.append(
        measure(
          f"{label}/{leaves}",
          call,
          calls=max(1, args.calls // leaves),
          repeats=args.repeats,
        )
      )
  for label, call in (
    ("multiaxis", partial(multiaxis, np.ones((2, 3, 4, 3), dtype=np.float32))),
    ("variadic", partial(variadic, np.ones((2, 3, 4, 3), dtype=np.float32))),
    ("like-cast", partial(like, np.ones(3, dtype=np.int32))),
    ("extract-dtype", partial(extract_dtype_str, np.ones(3, dtype=np.float32))),
    ("match-dtype", partial(FLOAT32.matches, np.ones(3, dtype=np.float32))),
  ):
    results.append(measure(label, call, calls=args.calls, repeats=args.repeats))
  results.extend(
    measure(
      function.__name__, function, calls=min(args.calls, 1_000), repeats=args.repeats
    )
    for function in (
      decorate_array,
      construct_tree_validator,
      construct_array_validator,
    )
  )
  evidence = {
    "python": sys.version,
    "platform": platform.platform(),
    "machine": platform.machine(),
    "bearshape_origin": bearshape.__file__,
    "versions": {
      package: version(package)
      for package in ("bearshape", "beartype", "numpy", "optree")
    },
    "results": results,
  }
  json.dump(evidence, sys.stdout, indent=2)
  sys.stdout.write("\n")


if __name__ == "__main__":
  main()
