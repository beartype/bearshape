"""Record or verify the exact archives, source and workflow of a candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


def verify_evidence(
  evidence: dict[str, str],
  directory: Path,
  *,
  source_sha: str,
  version: str,
  run_url: str,
) -> None:
  """Reject different identities, extra files, unsafe names or changed bytes."""
  if re.fullmatch(r"[0-9a-f]{40}", source_sha) is None:
    message = "Source identity must be a full commit SHA"
    raise ValueError(message)
  expected = {"source_sha": source_sha, "version": version, "run_url": run_url}
  for key, value in expected.items():
    if evidence.get(key) != value:
      message = f"Release evidence {key} differs from this validation run"
      raise ValueError(message)
  canonical = {
    "wheel": f"bearshape-{version}-py3-none-any.whl",
    "sdist": f"bearshape-{version}.tar.gz",
  }
  if any(evidence.get(kind) != name for kind, name in canonical.items()):
    message = "Release evidence must name the canonical wheel and source archive"
    raise ValueError(message)
  if {path.name for path in directory.iterdir()} != set(canonical.values()):
    message = "Distribution directory must contain exactly the two validated archives"
    raise ValueError(message)
  for kind in ("wheel", "sdist"):
    path = directory / evidence[kind]
    if path.is_symlink() or not path.is_file():
      message = f"Release archive must be a regular file: {path.name}"
      raise ValueError(message)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if evidence.get(f"{kind}_sha256") != digest:
      message = f"Release archive hash differs from validated evidence: {path.name}"
      raise ValueError(message)


def main() -> None:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("mode", choices=("record", "verify"))
  parser.add_argument("manifest", type=Path)
  parser.add_argument("directory", type=Path)
  parser.add_argument("--source-sha", required=True)
  parser.add_argument("--version", required=True)
  parser.add_argument("--run-url", required=True)
  args = parser.parse_args()
  if args.mode == "record":
    from check_distribution import check_distribution

    evidence = check_distribution(
      args.directory / f"bearshape-{args.version}-py3-none-any.whl",
      args.directory / f"bearshape-{args.version}.tar.gz",
    )
    evidence.update(source_sha=args.source_sha, run_url=args.run_url)
  else:
    evidence = json.loads(args.manifest.read_text(encoding="utf-8"))
  verify_evidence(
    evidence,
    args.directory,
    source_sha=args.source_sha,
    version=args.version,
    run_url=args.run_url,
  )
  if args.mode == "record":
    args.manifest.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
  sys.stdout.write(json.dumps(evidence, indent=2) + "\n")


if __name__ == "__main__":
  main()
