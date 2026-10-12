# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

The next candidate is **0.1.0rc1**, independently versioned from beartype and
not yet published. Python **3.11+** is required; the validated matrix is
**3.11–3.14**, with exact released beartype **0.23.1** as the current baseline
and dependency range `>=0.23.1,<0.24`. Full native composite-union rollback
still requires supported upstream integration before release. Local patches are
proposal evidence only.

### Fixed

- Preserve grouping and runtime Value scope in nested arithmetic, reflected
    operators, attributes and powers of negative dimensions.
- Retain strict variadic targets when mixed with broadcastable occurrences,
    including equal-shape transitions and returns. Custom variadic broadcasting
    does not import NumPy.
- Isolate independent public checks inside Tree predicates while preserving
    cross-leaf dimensions, structures and enclosing Value arguments. Check
    suffix constraints along every ragged path, including shallow leaves and
    empty containers, and reject interior/repeated ellipses.
- Validate custom array metadata with nonnegative integer-index axes. Turn
    ordinary property/metadata failures into useful diagnostics while allowing
    cancellation to propagate. Like converters own untrusted input inspection;
    reject malformed results and preserve original arguments.
- Honor each backend's selected Like converter for layouts, byte order, dtypes
    and foreign protocols. Do not retry failures through another backend.
- Release temporary classes from the default Like trust cache with weak keys.
- Keep validation state owned by its active invocation, restore failed atomic
    checks and diagnostic changes, and avoid retaining checked arrays. The
    broader native composite-union boundary remains the upstream release gate.
- Make `bearshape_this_package()` instrument the calling package's parameters
    and returns. Keep `check(conf=None)` aligned with its public overloads.
- Correct normal-install origin checks for symlinked virtual environments and
    report readable array/tree failures with the owning backend's hint names.

### Performance

- Prepare builtin dtype names and invariant shape traversal once per annotation
    while preserving custom metadata, live scopes and every Tree leaf check.
- Bind runtime arguments only for array annotations containing Value dimensions.
    Reuse owned Tree array validators while retaining all-leaf traversal,
    per-leaf snapshots and independent-check isolation.
- Filter unrelated frames before reading their locals. Preserve matched runtime
    samples, construction costs and artifact identities; timings are not a CI
    threshold. Checked-value and custom dtype metadata remain live; builtin
    dtype class names are prepared once by the later optimization.

### Typing and compatibility

- Check actual positive, negative and inference consumers with pyright, mypy, ty
    and pyrefly across Python 3.11–3.14. Missing required engines fail.
- Accept tested ordinary Like inputs for NumPy, JAX and Torch while retaining
    native results after explicit conversion. Allow nonnumeric NumPy dtypes in
    Shaped annotations.
- Model ordinary typed Tree leaves, lists, tuples, dictionaries and None;
    document runtime-only structure syntax and checker aliases for custom nodes.
- Test native TYPE_CHECKING aliases for complete custom/Structured annotations.
    Preserve NumPy result/dtype inference without claiming static shape or
    structured-field proofs. Native CuPy static support remains explicitly
    limited to the accepted protocol surface.
- Keep JAX jit/vmap/grad, Torch autograd/eager compiler boundaries, scalar/Like
    families, default optree registration and inherited check_context behavior
    covered and documented.

### CI and release tooling

- Upgrade the locked development tools, checkers, documentation and notebook
    tooling. Coordinate uv 0.13.0, its build backend, hooks and workflow pins
    while retaining Python 3.11 support and the existing compatibility floors.

- Share locked candidate validation across PRs, pushes, nightly and releases:
    CPU backends, four checkers, compatibility floors, coverage, docs, notebook,
    installed archives and minimal environments. Use the locked Ruff toolchain.

- Require the entire native composition/scope suite against the actual installed
    candidate and published dependency before releasing. The separate upstream
    proposal workflow cannot authorize publication.

- Add a separate latest-compatible runtime/backend canary with retained lock,
    source, versions and test evidence, without changing locked acceptance.

- Build wheels from source archives, verify licenses/typing markers/package
    contents, and test normal consumers outside the checkout. Ship the
    regression suite and its configuration in the source archive.

- Require immutable tag/version/source identity and verified artifact hashes
    before OIDC trusted publishing. Support validation-only runs and document
    developer preparation, approval, upload and recovery. Final CUDA evidence
    must match the exact final wheel.

- Keep Pages deployment manually authorized while building/packaging docs in CI.
    Use reviewed Node 24 actions and preserve rendered tables/admonitions.

- Scope file hooks to pre-commit, remove the unused commit-message hook, clear
    inherited Git repository variables in release tooling, and test hook stages.

### Maintenance

- Complete the lowercase bearshape rename and transfer GitHub/documentation
    identities to `beartype/bearshape` and `beartype.github.io/bearshape`.
    Preserve original authorship and historical evidence; private PyPI trust
    remains a separate verification.
- Align shared agent guidance, execution plans, contributor commands and
    maintainer handoff with current ownership and validation responsibilities.
- Use the required typing backports on supported interpreters, and build the
    documentation with Zensical while preserving the established site design.

### Documentation

- Distinguish the unpublished candidate from the PyPI release, document the
    union limitation and correct public factory, Like and decorator examples.
- Complete the contributor review workflow, validation recipes and current
    handoff while retaining clearly marked historical evidence.

## [0.0.1] - 2026-03-31

### Added

- Runtime shape and dtype validation for NumPy, JAX, PyTorch, and CuPy arrays,
    powered by `typing.Annotated` and beartype validators.
- Symbolic dimension syntax including named dimensions, anonymous dimensions,
    `Scalar`, arithmetic dimension expressions, and constrained `Value(...)`
    checks.
- `Tree[...]` validation helpers, explicit `@bearshape.check` support, and
    `check_context()` for shared manual bearability checks.
- Multi-checker typing coverage across pyright, mypy, and ty, with CI, tox, and
    pre-commit validation for runtime and typing behavior.
- A documentation website covering installation, API boundaries, supported
    backends, and practical usage patterns.

### Notes

- The root `bearshape` module intentionally stays lightweight and
    optional-dependency-safe; backend-specific aliases and factories live in
    `bearshape.numpy`, `bearshape.jax`, `bearshape.torch`, and `bearshape.cupy`.
- CuPy support remains optional at install time and requires a compatible CuPy
    environment when used at runtime.
