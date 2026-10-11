"""Build and validate reviewed upstream patches without changing the lock."""

# All subprocesses use argument lists, never a shell.
# ruff: noqa: S404, S603

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from check_installed import _copy_consumers
from check_release import git_environment

ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = ROOT / "tools" / "upstream"


ORIGIN_CHECK = (
  "import beartype,bearshape,pathlib,sys; "
  "print(sys.version); "
  "print(beartype.__file__); print(bearshape.__file__); "
  "assert all(pathlib.Path(m.__file__).resolve().is_relative_to("
  "pathlib.Path(sys.prefix).resolve()) for m in (beartype,bearshape)); "
  "from beartype.plug import get_hint_check_scope; "
  "assert get_hint_check_scope() is None"
)


def _apply_patches(
  source: Path, git: str, environment: dict[str, str], parser: argparse.ArgumentParser
) -> dict:
  manifest = json.loads((PROPOSAL / "patches" / "series.json").read_text())
  head = subprocess.check_output(
    [git, "rev-parse", "HEAD"], cwd=source, env=environment, text=True
  ).strip()
  dirty = subprocess.check_output(
    [git, "status", "--porcelain"], cwd=source, env=environment, text=True
  )
  if head != manifest["base_commit"] or dirty:
    parser.error("upstream source must be clean at the manifest base commit")
  for entry in manifest["patches"]:
    patch = PROPOSAL / "patches" / entry["file"]
    if patch.parent != PROPOSAL / "patches" or patch.suffix != ".patch":
      parser.error("patch must name a file directly in the patches directory")
    if hashlib.sha256(patch.read_bytes()).hexdigest() != entry["sha256"]:
      parser.error(f"patch digest differs: {patch.name}")
    subprocess.run(
      [git, "apply", "--check", str(patch)], cwd=source, env=environment, check=True
    )
    subprocess.run([git, "apply", str(patch)], cwd=source, env=environment, check=True)
  return manifest


def main() -> None:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("--upstream-source", type=Path, required=True)
  parser.add_argument("--output", type=Path, required=True)
  parser.add_argument("--python", required=True)
  args = parser.parse_args()
  uv, git = shutil.which("uv"), shutil.which("git")
  if uv is None or git is None:
    parser.error("uv and git are required")
  args.upstream_source = args.upstream_source.resolve()
  output = args.output.resolve()
  output.mkdir(parents=True, exist_ok=False)
  environment = git_environment(git)
  for key in ("PYTHONPATH", "PYTHONHOME", "TOX_ENV_NAME"):
    environment.pop(key, None)
  environment["UV_TORCH_BACKEND"] = "cpu"
  commands = []

  def run(command: list[str], cwd: Path = output) -> None:
    commands.append({"command": command, "cwd": str(cwd)})
    (output / "commands.json").write_text(json.dumps(commands, indent=2) + "\n")
    subprocess.run(command, cwd=cwd, env=environment, check=True)

  manifest = _apply_patches(args.upstream_source, git, environment, parser)
  dist = output / "dist"
  run([uv, "build", "--wheel", "--out-dir", str(dist), str(args.upstream_source)])
  run([uv, "build", "--sdist", "--out-dir", str(dist), str(ROOT)])
  sdist = next(dist.glob("bearshape-*.tar.gz"))
  run([uv, "build", "--wheel", "--out-dir", str(dist), str(sdist)])
  consumer = output / "consumer"
  consumer.mkdir()
  _copy_consumers(sdist, consumer)
  requirements = output / "requirements.txt"
  run(
    [
      uv,
      "export",
      "--locked",
      "--no-hashes",
      "--no-emit-project",
      "--no-emit-package",
      "beartype",
      "--output-file",
      str(requirements),
    ],
    consumer,
  )
  run([uv, "venv", str(output / "venv"), "--python", args.python])
  python = str(
    output / "venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
  )
  run([
    uv,
    "pip",
    "install",
    "--python",
    python,
    "-r",
    str(requirements),
    *map(str, sorted(dist.glob("*.whl"))),
  ])
  run([python, "-I", "-c", ORIGIN_CHECK])
  protocol = consumer / "tools" / "upstream" / "protocol"
  protocol.mkdir()
  for test in (args.upstream_source / "beartype_test/a00_unit/a40_api/plug").glob(
    "test_plug*.py"
  ):
    if test.name != "test_plughintable.py":
      shutil.copyfile(test, protocol / test.name)
  run([python, "-I", "tools/validate_runtime.py", "cpu"], consumer)
  run([python, "-I", "tools/probe_union.py"], consumer)
  run(
    [
      python,
      "-I",
      "-m",
      "pytest",
      "tests/",
      "tools/upstream/",
      "--installed-package",
      "-n",
      "auto",
    ],
    consumer,
  )
  evidence = {
    "base_commit": manifest["base_commit"],
    "patches": manifest["patches"],
    "artifacts": {
      file.name: hashlib.sha256(file.read_bytes()).hexdigest()
      for file in sorted(dist.iterdir())
    },
    "status": "passed",
    "published_dependency": False,
  }
  (output / "evidence.json").write_text(json.dumps(evidence, indent=2) + "\n")
  json.dump(evidence, sys.stdout, indent=2)
  sys.stdout.write("\n")


if __name__ == "__main__":
  main()
