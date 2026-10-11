# Scope and transaction design review

This review targets beartype v0.23.1 (`f85b67d8`) and the ordered patches in
`patches/series.json`. The implementation is a proposal for upstream review, not
a supported dependency release. The performance delta remains separate in #47.

## Isolation correction

The previous scope implementation distinguished public invocations, but its
transaction stack enrolled every nested state getter into every active parent.
When an independent check used a getter before an outer forward alias resolved,
the parent retained the inner state object. Its eventual rollback then missed
the outer binding. A valid fallback union could fail a later shape check.

Transactions now record the identity of their live public checking frame and
enroll only into live parents with the same identity. Internal alias delegates
skip their own boundary and therefore join the caller. Public DOOR calls and
nested decorated calls have different owners, including recursive calls through
the same wrapper code. The private identifier is cleared on exit; no transaction
retains a frame. An active parent's frame cannot be recycled, and completed
parents retained by copied contexts are ignored.

The existing boundary traversal is shared by the public scope accessor and the
private owner lookup. Ownership does not allocate a `HintCheckScope`. The public
API is unchanged: `get_hint_check_scope()` returns a scope with `state`, lazy
`arguments`, and `owner_code`, or `None` outside checking. `owner_code`
identifies the generated entry point for explicit decorator integration; only
scope object identity distinguishes invocations. Plugins should use a private
object key in `state`, and must not retain scopes after checking.

## Alternatives considered

- Getter identity alone is incorrect: one getter locates different state in
    different invocations.
- State identity alone is insufficient: it still lets one invocation roll back
    another's independent successful state.
- Allocating a public scope for every transaction could provide identity, but
    adds allocation for ordinary unresolved references and weakens lazy
    creation.
- A ContextVar boundary around every wrapper could isolate ownership, but adds
    entry/exit machinery to ordinary calls and expands async/cancellation
    handling.
- Wrapper code identity is incorrect for recursion: separate invocations share a
    code object.
- Reusing the boundary lookup and retaining only a private identifier is the
    chosen correction. It needs no new public surface, retained frames or
    ordinary public-scope allocation.

Leaf-only rollback, resetting the whole call, rewriting annotations and retrying
validators do not preserve all earlier bindings, native composition, ordering
and side effects. Existing hint-reduction hooks transform hints but cannot
observe the success or failure of an enclosing union branch. An explicit
configuration flag would change bearshape's existing bare `@beartype` contract
for late aliases. These alternatives were evaluated against that contract; this
is not a claim that all possible designs have been exhaustively proved inferior.

## Compatibility with upstream implementation

The proposal keeps beartype's native expression generator and union ordering. It
adds checkpoints at the boundaries owned by that generator, keeps its random
sample value, and compiles transactional expressions once. Forward proxies keep
native lazy resolution. Composite aliases use the existing DOOR code factory
through a separate internal cache: the current cache key does not include the
code factory, so sharing the public cache would mix scope semantics.

Diagnostic traversal uses the same state protocol and restores its exploratory
mutations. The existing special paths for `NoReturn` and legacy tuple unions are
preserved. The snapshot token is opaque; a plugin getter locates state, while
`snapshot()` and `restore(token)` implement rollback. Python's bare `isinstance`
does not gain this protocol, so bearshape retains its leaf guarantees.

PR #47 keeps known-domain transactions unpublished and consults owner identity
only when a parent exists. Its ordinary composite specialization waits for
natural resolution to plain classes, captures those classes, and invalidates
through the existing reference cache. It never eagerly resolves an unused
alternative or replays a predicate. Root references and single sampled-reference
lists retain native proxy checking. Atomic-leaf optimization remains an explicit
plugin promise; custom metaclasses and stateful aliases keep the general path.

The full proposal touches code generation, aliases, diagnostics and caches; it
should not be presented as a trivial one-hook change. The isolation correction
itself changes only the scope lookup and transaction enrollment. Native checks
without state or relevant references do not walk scopes. Ordinary reference
users still have hook lookup and cold/general-path costs. The performance PR
measures those costs rather than claiming universal zero overhead.

## Evidence and remaining limits

The preserved candidate fails eight of 17 new generic isolation cases. The
corrected build passes all 17, plus 24 bearshape cases covering nested public
testers, raisers, decorated calls, both discovery orders, caught failures and
automatic/explicit memo scopes. The generic suite also covers recursion, copied
active contexts in another thread, successful and failed object release, and
absence of public scope allocation for ordinary checks. Existing alias, async,
union, error, sampling and cache regressions remain required.

The plan records fresh installed consumers and upstream results on CPython 3.11
and 3.14. Those endpoints and local macOS measurements do not prove every
interpreter, platform or optional backend. Hosted CI provides additional
coverage. Upstream review of the public API and integration remains necessary;
there has been no maintainer contact, upstream PR, main merge or publication.
