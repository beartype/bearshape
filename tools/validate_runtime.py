"""Fail early when a required candidate backend is missing or incorrectly built."""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import json
import sys

_BACKENDS = ("numpy", "jax", "torch", "optree")


def _require_beartype_version(version: str, *, latest_compatible: bool) -> None:
  if not latest_compatible:
    if version != "0.23.1":
      message = f"expected beartype 0.23.1, found {version}"
      raise SystemExit(message)
    return

  from packaging.requirements import Requirement

  for raw in importlib.metadata.requires("bearshape") or ():
    requirement = Requirement(raw)
    if requirement.name == "beartype":
      if requirement.specifier.contains(version, prereleases=False):
        return
      message = f"beartype {version} does not satisfy {requirement}"
      raise SystemExit(message)
  message = "installed bearshape metadata does not declare beartype"
  raise SystemExit(message)


def main() -> None:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("environment", nargs="?", default="cpu")
  parser.add_argument(
    "--latest-compatible",
    action="store_true",
    help="Canary only: require the installed package's dependency range instead of the exact baseline",
  )
  args = parser.parse_args()
  factors = args.environment.split("-")
  if any(factor in {"cpu", "dev", "type"} for factor in factors):
    backends = _BACKENDS
  else:
    backends = tuple(
      name for name in _BACKENDS if any(f.startswith(name) for f in factors)
    )
  if not backends:
    parser.error(f"no expected backend in {args.environment!r}")

  versions = {}
  for name in ("bearshape", "beartype", *backends):
    module = importlib.import_module(name)
    versions[name] = {
      "version": module.__version__,
      "path": module.__file__,
    }
    if name == "beartype":
      _require_beartype_version(
        module.__version__, latest_compatible=args.latest_compatible
      )
    if name == "torch" and (
      module.version.cuda is not None or module.version.hip is not None
    ):
      message = "CPU validation requires a CPU-only Torch build"
      raise SystemExit(message)
  sys.stdout.write(
    json.dumps({"python": sys.version, "modules": versions}, indent=2) + "\n"
  )


if __name__ == "__main__":
  main()
