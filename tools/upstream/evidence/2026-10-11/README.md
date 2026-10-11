# Scope and optimization measurements

Matched sequential local runs on macOS arm64, Python 3.11.15 and 3.14.5, NumPy
2.4.6 and optree 0.19.1. Each warm median uses 20,000 calls and seven raw
repeats. All variants use the same bearshape wheel; only the upstream wheel
changes. The shared `benchmark_transactions.py` checks correctness before
timing. Invalid published-baseline union cases are recorded as incorrect, not
faster valid runs. First invocations are single setup observations, not
cold-start distributions.

Each JSON file records the script hash, both wheel hashes, interpreter,
platform, versions, every raw repeat and correctness result. Published wheel
package files were compared byte-for-byte with the PyPI wheel in both baseline
environments. The correctness source is local upstream commit `5071616b`;
optimized source is `01f32470`. Ordered patches against released `f85b67d8` are
in `../../patches/`. The implementation source is bearshape commit `291af356`;
later evidence changes do not change the tested runtime files. All 17 runtime
source files were compared with the tested wheel. These are local proposal
wheels, not upstream releases.

Times below are microseconds per call.

| Case           | Python |  Released | Correctness | Optimized |
| -------------- | ------ | --------: | ----------: | --------: |
| native         | 3.11   |     0.092 |       0.094 |     0.096 |
| native         | 3.14   |     0.093 |       0.093 |     0.095 |
| Root ref       | 3.11   |     0.636 |       0.685 |     0.704 |
| Root ref       | 3.14   |     0.498 |       0.492 |     0.502 |
| Sampled list   | 3.11   |     0.683 |       1.108 |     0.745 |
| Sampled list   | 3.14   |     0.536 |       0.915 |     0.563 |
| Tuple          | 3.11   |     0.672 |       1.107 |     0.162 |
| Tuple          | 3.14   |     0.520 |       0.865 |     0.176 |
| Mapping        | 3.11   |     0.693 |       1.126 |     0.193 |
| Mapping        | 3.14   |     0.569 |       0.910 |     0.214 |
| Nested lists   | 3.11   |     0.723 |       1.147 |     0.213 |
| Nested lists   | 3.14   |     0.590 |       0.944 |     0.245 |
| strict         | 3.11   |    12.572 |       9.816 |     7.600 |
| strict         | 3.14   |    12.875 |      10.313 |     7.905 |
| explicit       | 3.11   |     8.292 |       8.190 |     6.044 |
| explicit       | 3.14   |     7.802 |       8.707 |     6.459 |
| Union fallback | 3.11   | Incorrect |      13.491 |    12.205 |
| Union fallback | 3.14   | Incorrect |      14.048 |    12.482 |

The warm tuple/mapping/nested-list cases are faster than both earlier variants.
Native checks remain around 0.09 microseconds, with a few nanoseconds of local
variation. Root references and the simple sampled list retain proxy checking: on
3.11 their additional cost is about 0.06–0.07 microseconds relative to released
0.23.1. Custom metaclasses and stateful/composite aliases deliberately retain
the general path; these results do not claim that all possible annotations are
faster. The first successful composite check still performs normal resolution
and may compile its specialization. State-hook metadata must remain stable until
cache invalidation, as with other compiled hint metadata. No timing threshold is
used.

Fresh normally installed optimized endpoint suites passed 1,221 cases each,
including all four checker consumers; five skips identify absent CuPy and four
platform precision cases. Correctness-only suites passed 1,210 each. Upstream
unit suites passed 467/475 optimized cases and 456/464 correctness cases, with
15/7 interpreter or optional-dependency skips. Upstream pyright passed. The
optimizer adds eleven cases covering invalidation, concurrent clearing, retained
classes, unselected aliases, known-domain contexts, atomic leaves and
sampling/predicates.

The full commands, exact archives, imported paths and logs are preserved under
the main checkout's ignored `build/union-scope-development/`. Proposal workflow
artifacts provide independently built hosted evidence. No package publication,
upstream PR, maintainer message or main merge is part of these results.
