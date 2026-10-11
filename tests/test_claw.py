"""Exercise caller-package instrumentation in independent Python processes."""

from __future__ import annotations

import subprocess
import sys
import textwrap
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
  from pathlib import Path


@pytest.mark.parametrize("custom_conf", [False, True])
def test_instruments_caller_package(tmp_path: Path, custom_conf: bool) -> None:
  package = tmp_path / "instrumented"
  nested = package / "nested"
  nested.mkdir(parents=True)
  conf = (
    "BeartypeConf(violation_param_type=ValueError, "
    "violation_return_type=TypeError, is_color=False)"
    if custom_conf
    else "BeartypeConf(is_color=False)"
  )
  (package / "__init__.py").write_text(
    "from beartype import BeartypeConf\n"
    "from bearshape.claw import bearshape_this_package\n"
    f"bearshape_this_package(conf={conf})\n"
  )
  (nested / "__init__.py").write_text("")
  (nested / "arrays.py").write_text(
    textwrap.dedent("""\
      import numpy as np
      from bearshape import N
      from bearshape.numpy import F32

      def agree(x: F32[N], y: F32[N]) -> F32[N]:
          return y

      def wrong_return(x: F32[N]) -> F32[N]:
          return np.ones(x.shape[0] + 1, dtype=np.float32)
      """)
  )
  (tmp_path / "unrelated.py").write_text(
    "def unchecked(value: int) -> int:\n    return value\n"
  )
  param_error = "ValueError" if custom_conf else "BeartypeCallHintParamViolation"
  return_error = "TypeError" if custom_conf else "BeartypeCallHintReturnViolation"
  script = textwrap.dedent(f"""\
    import numpy as np
    from beartype.roar import (
        BeartypeCallHintParamViolation, BeartypeCallHintReturnViolation,
    )
    from instrumented.nested.arrays import agree, wrong_return
    from unrelated import unchecked

    a = np.ones(2, dtype=np.float32)
    b = np.ones(3, dtype=np.float32)
    assert agree(a, a) is a
    assert unchecked('still unchecked') == 'still unchecked'
    try:
        agree(a, b)
    except {param_error}:
        pass
    else:
        raise AssertionError('caller-package parameter was not checked')
    try:
        wrong_return(a)
    except {return_error}:
        pass
    else:
        raise AssertionError('caller-package return was not checked')
    """)
  result = subprocess.run(
    [sys.executable, "-c", script],
    cwd=tmp_path,
    capture_output=True,
    text=True,
    timeout=30,
  )
  assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("competing_hook", [False, True])
def test_public_inactive_hook_diagnostic(competing_hook: bool) -> None:
  script = textwrap.dedent(f"""\
    import sys
    import warnings
    from importlib.machinery import FileFinder, SourceFileLoader, SOURCE_SUFFIXES
    from beartype.claw import beartype_package, warn_if_beartype_claw_inactive
    from beartype.roar import BeartypeClawImportlibFileFinderPathHookInactiveWarning
    from bearshape.claw import bearshape_this_package
    from beartype.claw import beartype_this_package

    assert bearshape_this_package is beartype_this_package
    beartype_package('unused_diagnostic_test_package')
    if {competing_hook!r}:
        sys.path_hooks.insert(0, FileFinder.path_hook((SourceFileLoader, SOURCE_SUFFIXES)))
        sys.path_importer_cache.clear()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        warn_if_beartype_claw_inactive()
    relevant = [w for w in caught if issubclass(
        w.category, BeartypeClawImportlibFileFinderPathHookInactiveWarning)]
    assert bool(relevant) is {competing_hook!r}, caught
    """)
  result = subprocess.run(
    [sys.executable, "-c", script], capture_output=True, text=True, timeout=30
  )
  assert result.returncode == 0, result.stdout + result.stderr
