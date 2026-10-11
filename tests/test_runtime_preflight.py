"""The dependency canary cannot weaken exact release preflight validation."""

import importlib.metadata
import runpy
from pathlib import Path

import pytest

_MODULE = runpy.run_path(
  str(Path(__file__).resolve().parents[1] / "tools/validate_runtime.py")
)


@pytest.mark.parametrize(
  "version, compatible, accepted",
  [
    ("0.23.1", False, True),
    ("0.23.2", False, False),
    ("0.23.2", True, True),
    ("0.22.9", True, False),
    ("0.24.0", True, False),
    ("0.24.0rc1", True, False),
  ],
)
def test_beartype_preflight_policy(
  monkeypatch: pytest.MonkeyPatch, version: str, *, compatible: bool, accepted: bool
) -> None:
  monkeypatch.setattr(
    importlib.metadata, "requires", lambda _name: ["beartype>=0.23.1,<0.24"]
  )
  check = _MODULE["_require_beartype_version"]
  if accepted:
    check(version, latest_compatible=compatible)
  else:
    with pytest.raises(SystemExit, match="beartype"):
      check(version, latest_compatible=compatible)


def test_canary_reads_installed_dependency_contract(
  monkeypatch: pytest.MonkeyPatch,
) -> None:
  monkeypatch.setattr(
    importlib.metadata, "requires", lambda _name: ["beartype>=0.24,<0.25"]
  )
  _MODULE["_require_beartype_version"]("0.24.1", latest_compatible=True)


def test_canary_requires_dependency_metadata(monkeypatch: pytest.MonkeyPatch) -> None:
  monkeypatch.setattr(importlib.metadata, "requires", lambda _name: None)
  with pytest.raises(SystemExit, match="beartype"):
    _MODULE["_require_beartype_version"]("0.23.1", latest_compatible=True)
